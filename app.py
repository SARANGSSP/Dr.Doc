from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import fitz  # PyMuPDF
import os
import tempfile

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# Configure Gemini
genai.configure(api_key="AIzaSyAk66YEWMG0vZerNB4dSnxD6HXddIVXCNE")
model = genai.GenerativeModel("models/gemini-pro")

@app.route("/")
def home():
    return app.send_static_file("summary.html")

@app.route("/highlight", methods=["POST"])
def highlight_pdf():
    try:
        from geminibhadwa import input_pdf_path, output_pdf_path, highlight_rgb, skip_rgb, main

        pdf_file = request.files["pdf"]
        highlight_hex = request.form.get("highlight_color", "#22C55E")
        skippable_hex = request.form.get("skippable_color", "#EF4444")

        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip("#")
            return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))

        highlight_rgb[:] = hex_to_rgb(highlight_hex)
        skip_rgb[:] = hex_to_rgb(skippable_hex)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
            pdf_file.save(temp_input.name)
            input_path = temp_input.name

        output_path = input_path.replace(".pdf", "_highlighted.pdf")

        import geminibhadwa
        geminibhadwa.input_pdf_path = input_path
        geminibhadwa.output_pdf_path = output_path

        main()

        return jsonify({
            "download_url": f"/download/{os.path.basename(output_path)}"
        })

    except Exception as e:
        print("❌ Highlighting error:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_file(filename):
    directory = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
