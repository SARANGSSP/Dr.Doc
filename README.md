Certainly! Here's a more formal, polished, and professional version of your `README.md`:

---

# 📄 Gemini-Powered PDF Highlighter and Question Generator

## Overview

This repository hosts a web application designed to process PDF files and generate educational resources. The application offers the following capabilities:

- **AI-powered highlighting**: Identify and annotate important content in a PDF, distinguishing it from skippable sections.
- **Exam question generation**: Create multiple-choice questions (MCQs), short-answer, and long-answer questions using Gemini AI (Pro versions 1.5 and 2.5).
- **Custom color-coded annotations**: Annotate content in PDFs with personalized color schemes utilizing PyMuPDF.

---

## Features

- **Effortless PDF uploading**: Enables users to upload PDF files seamlessly.
- **AI classification**: Automatically identifies important and skippable content.
- **Custom sentence-level highlighting**: Provides annotations with user-defined color schemes.
- **Question generation**: Produces exam-style questions via Gemini AI.
- **Modern architecture**: Flask backend integrated with an HTML/JavaScript frontend.

---

## Technical Stack

| **Component**      | **Technology Used**         |
|---------------------|-----------------------------|
| Backend             | Python, Flask              |
| PDF Processing      | PyMuPDF (fitz)             |
| AI Model            | Gemini Pro versions 1.5/2.5|
| Frontend            | HTML, CSS, JavaScript      |
| Highlighting Logic  | RapidFuzz (text match)     |

---

## Project Structure

```
├── app.py               # Flask backend server
├── geminibhadwa.py      # Logic for Gemini prompt and content classification
├── summary.html         # Main frontend interface
├── scripts.js           # JavaScript for frontend interaction
├── style.css            # General styling
├── summary.css          # Highlighting-specific styles
├── static/              # Directory for static assets (JS/CSS)
├── templates/           # Directory for HTML templates rendered by Flask
```

---

## Setup Instructions

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/gemini-pdf-highlighter.git
cd gemini-pdf-highlighter
```

### Step 2: Install dependencies

Ensure that Python (version 3.9 or higher) and `pip` are installed on your system. Then execute:

```bash
pip install -r requirements.txt
```

**For Anaconda users (recommended for Windows):**

```bash
conda create -n gemini-pdf python=3.10
conda activate gemini-pdf
conda install -c conda-forge pymupdf flask
```

### Step 3: Configure the Gemini API key

Add your Gemini API key by creating a `.env` file or by directly setting the key in `geminibhadwa.py`:

```python
genai.configure(api_key="YOUR_API_KEY")
```

---

## Execution

Start the application server by executing:

```bash
python app.py
```

Access the application via your web browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Future Enhancements

- [ ] Support for multi-page PDFs.
- [ ] Drag-and-drop functionality for uploading PDFs.
- [ ] Ability to save annotated PDFs with highlights.
- [ ] Enhanced difficulty-level detection for generated questions.


## License

This project is licensed under the **MIT License**. Please review the LICENSE file for more information.

---

## Contributions

Contributions are welcome! You can fork the repository and submit pull requests to improve the application. Feedback and issues can be reported via GitHub.

---

This version is more formal and structured while maintaining clarity and professionalism. Let me know if you'd like further adjustments or additions! 😊
