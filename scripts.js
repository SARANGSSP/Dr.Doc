const uploadArea = document.getElementById("upload-area");
const fileInput = document.getElementById("file-upload");
const fileNameDisplay = document.getElementById("file-name");
const generateBtn = document.getElementById("generate-btn");
const downloadBtn = document.getElementById("download-btn");

let selectedFile = null;

uploadArea.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    selectedFile = fileInput.files[0];
    fileNameDisplay.textContent = "✅ " + selectedFile.name;
  }
});

// Prevent default drag behavior
["dragenter", "dragover", "dragleave", "drop"].forEach(event =>
  uploadArea.addEventListener(event, e => e.preventDefault())
);

// Highlight on drag
uploadArea.addEventListener("dragover", () => {
  uploadArea.classList.add("hover");
});

uploadArea.addEventListener("dragleave", () => {
  uploadArea.classList.remove("hover");
});

uploadArea.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) {
    fileInput.files = e.dataTransfer.files;
    selectedFile = file;
    fileNameDisplay.textContent = "✅ " + file.name;
  }
  uploadArea.classList.remove("hover");
});

generateBtn.addEventListener("click", async () => {
  if (!selectedFile) {
    alert("Please upload a file first.");
    return;
  }

  const formData = new FormData();
  formData.append("pdf", selectedFile);
  formData.append("highlight_color", document.getElementById("theme-color").value);
  formData.append("skippable_color", document.getElementById("secondary-color").value);

  generateBtn.disabled = true;
  generateBtn.textContent = "Processing...";
  downloadBtn.style.display = "none";

  try {
    const response = await fetch("/highlight", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (response.ok && data.download_url) {
      downloadBtn.href = data.download_url;
      downloadBtn.style.display = "inline-block";
    } else {
      alert("❌ Failed to generate summary.");
    }
  } catch (err) {
    console.error(err);
    alert("❌ Error while processing PDF.");
  } finally {
    generateBtn.disabled = false;
    generateBtn.textContent = "Generate Summary";
  }
});
