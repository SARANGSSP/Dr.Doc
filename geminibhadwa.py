import fitz  # PyMuPDF
import pathlib
import re
import os
from rapidfuzz import fuzz
from google import genai

# === 🔐 Gemini API Key ===
genai_client = genai.Client(api_key="AIzaSyAk66YEWMG0vZerNB4dSnxD6HXddIVXCNE")  # Replace with your key

# === Prompts (5 pages at a time) ===
IMPORTANT_SPANS_PROMPT = """
You are a professor reviewing educational PDF materials.

Analyze the following text from 5 pages of a document. Extract and return a Python list called `important_spans` containing only key sentences or phrases (not full paragraphs unless necessary). These should reflect definitions, facts, or critical terminology. Escape formatting and special characters.

Return only the list. Do not include skippable or neutral content.
"""

SKIPPABLE_SPANS_PROMPT = """
You are a professor reviewing educational PDF materials.

Analyze the following text from 5 pages of a document. Extract and return a Python list called `skippable_spans` containing vague, filler, redundant, or low-relevance content. Keep it granular (sentence or phrase level). Escape formatting and special characters.

Return only the list. Do not include important or neutral content.
"""

# === Flask-integrated global variables ===
input_pdf_path = None
output_pdf_path = None
highlight_rgb = [0.2, 0.8, 0.4]
skip_rgb = [1.0, 0.0, 0.0]


# === 🔍 Split PDF text into 5-page chunks ===
def extract_page_chunks(pdf_path: pathlib.Path, chunk_size=5) -> list[str]:
    doc = fitz.open(str(pdf_path))
    chunks = []
    for i in range(0, len(doc), chunk_size):
        chunk_text = ""
        for j in range(i, min(i + chunk_size, len(doc))):
            chunk_text += doc[j].get_text()
        chunks.append(chunk_text)
    return chunks

# === 🧠 Ask Gemini + Extract Python list ===
def classify_spans(text: str, prompt: str, list_name: str) -> list[str]:
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-pro-exp-03-25",
            contents=[{"text": prompt + "\n\n" + text}]
        ).text
        code = extract_code_block(response)
        exec_globals = {}
        exec(code, {}, exec_globals)
        return exec_globals.get(list_name, [])
    except Exception as e:
        print(f"❌ Gemini failed for `{list_name}`: {e}")
        return []

# === 🧽 Deduplicate red against green ===
def deduplicate_skippable(important, skippable, overlap_threshold=85):
    cleaned_important = [clean(s) for s in important]
    filtered = []
    for skip in skippable:
        skip_clean = clean(skip)
        max_overlap = max((fuzz.ratio(skip_clean, imp) for imp in cleaned_important), default=0)
        if max_overlap < overlap_threshold:
            filtered.append(skip)
        else:
            print(f"🧽 Removed red (overlaps green): {skip[:80]}...")
    return filtered

# === ✂️ Clean words ===
def clean(word):
    return re.sub(r"[^\w/$]", "", word).lower()

# === Highlight spans in the full PDF ===
def highlight_spans(spans, doc, color_rgb, label):
    threshold = 85
    for span_index, span in enumerate(spans):
        reference = clean(span.strip())
        if not reference:
            continue
        matched = False

        for page_num, page in enumerate(doc, start=1):
            words = page.get_text("words")
            word_texts = [clean(w[4]) for w in words]

            best_score = 0
            best_start = None
            best_win_size = 0

            for i in range(len(word_texts)):
                for win_size in range(3, min(20, len(word_texts) - i)):
                    candidate_words = word_texts[i:i + win_size]
                    candidate = " ".join(candidate_words)
                    score = fuzz.ratio(candidate, reference)

                    if score > best_score:
                        best_score = score
                        best_start = i
                        best_win_size = win_size

            if best_score >= threshold and best_start is not None:
                rects = [fitz.Rect(words[best_start + j][0:4]) for j in range(best_win_size)]
                annot = page.add_highlight_annot(rects)
                annot.set_colors(stroke=color_rgb)
                annot.update()
                print(f"✅ {label} Match {span_index + 1} on page {page_num} ({best_score:.2f}%)")
                matched = True
                break

        if not matched:
            print(f"⚠️ {label} Match {span_index + 1} NOT found.")

# === Extract code block from Gemini response ===
def extract_code_block(text: str) -> str:
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

# === 🚀 Main Function (to be called from Flask) ===
def main():
    print("📄 Breaking document into 5-page chunks...")
    page_chunks = extract_page_chunks(input_pdf_path, chunk_size=5)

    all_important_spans = []
    all_skippable_spans = []

    for i, chunk in enumerate(page_chunks):
        print(f"\n🔎 Chunk {i + 1}/{len(page_chunks)} — important...")
        imp = classify_spans(chunk, IMPORTANT_SPANS_PROMPT, "important_spans")
        all_important_spans.extend(imp)

        print(f"🔎 Chunk {i + 1}/{len(page_chunks)} — skippable...")
        skip = classify_spans(chunk, SKIPPABLE_SPANS_PROMPT, "skippable_spans")
        all_skippable_spans.extend(skip)

    if all_important_spans and all_skippable_spans:
        print("\n🧹 Deduplicating overlapping red text...")
        all_skippable_spans = deduplicate_skippable(all_important_spans, all_skippable_spans)

    print("\n📄 Highlighting full document...")
    doc = fitz.open(str(input_pdf_path))

    if all_important_spans:
        print("🟢 Highlighting important spans...")
        highlight_spans(all_important_spans, doc, color_rgb=highlight_rgb, label="Green")

    if all_skippable_spans:
        print("🔴 Highlighting skippable spans...")
        highlight_spans(all_skippable_spans, doc, color_rgb=skip_rgb, label="Red")

    doc.save(output_pdf_path, garbage=4, deflate=True)
    print(f"\n✅ Done! PDF saved at: {output_pdf_path}")
