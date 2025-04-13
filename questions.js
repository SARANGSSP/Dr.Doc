const uploadArea = document.getElementById("upload-area");
const fileInput = document.getElementById("file-upload");
const fileNameDisplay = document.getElementById("file-name");
const createBtn = document.getElementById("create-btn");

let selectedFile = null;

uploadArea.addEventListener("click", () => fileInput.click());

uploadArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadArea.style.borderColor = "#00ffab";
});

uploadArea.addEventListener("dragleave", () => {
  uploadArea.style.borderColor = "rgba(255, 255, 255, 0.1)";
});

uploadArea.addEventListener("drop", (e) => {
  e.preventDefault();
  fileInput.files = e.dataTransfer.files;
  showFileName();
});

fileInput.addEventListener("change", showFileName);

function showFileName() {
  if (fileInput.files.length > 0) {
    selectedFile = fileInput.files[0];
    fileNameDisplay.innerHTML = `✅ ${selectedFile.name}`;
    fileNameDisplay.title = "Click to open";
    fileNameDisplay.onclick = () => {
      const fileURL = URL.createObjectURL(selectedFile);
      window.open(fileURL, "_blank");
    };
  } else {
    fileNameDisplay.innerHTML = '';
    fileNameDisplay.onclick = null;
  }
}

createBtn.addEventListener("click", async () => {
  if (!selectedFile) return alert("Please upload a PDF first.");

  const type = document.getElementById("question-type").value;
  const count = document.getElementById("importance").value;

  const formData = new FormData();
  formData.append("pdf", selectedFile);
  formData.append("question_type", type);
  formData.append("question_count", count);

  createBtn.disabled = true;
  createBtn.textContent = "Generating...";

  try {
    const response = await fetch("/generate-questions", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (response.ok) {
      showQuestions(data.questions);
    } else {
      alert("❌ Error: " + (data.error || "Something went wrong."));
    }
  } catch (err) {
    console.error(err);
    alert("❌ Failed to generate questions.");
  } finally {
    createBtn.disabled = false;
    createBtn.textContent = "Create Questions";
  }
});

function showQuestions(text) {
  let viewer = document.getElementById("question-viewer");
  if (!viewer) {
    viewer = document.createElement("div");
    viewer.id = "question-viewer";
    viewer.style.marginTop = "20px";
    viewer.style.whiteSpace = "pre-wrap";
    viewer.style.textAlign = "left";
    viewer.style.fontSize = "1rem";
    viewer.style.background = "rgba(255,255,255,0.05)";
    viewer.style.padding = "20px";
    viewer.style.borderRadius = "12px";
    viewer.style.maxHeight = "400px";
    viewer.style.overflowY = "auto";
    document.querySelector(".container").appendChild(viewer);
  }
  viewer.innerText = text;
  addDownloadButton(text);
}

function addDownloadButton(text) {
  let btn = document.getElementById("download-word");
  if (!btn) {
    btn = document.createElement("button");
    btn.id = "download-word";
    btn.textContent = "Download as Word";
    btn.style.marginTop = "15px";
    btn.className = "button";
    document.querySelector(".container").appendChild(btn);
  }
  btn.onclick = () => downloadAsWord(text);
}

function downloadAsWord(text) {
  const blob = new Blob(
    [`${text}`],
    { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" }
  );

  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "generated_questions.docx";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(link.href);
}
