
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from pathlib import Path
from parser import ResumeParser
import json
import tempfile

BASE_DIR = Path(__file__).resolve().parent

# Works on both Windows and Vercel
TEMP_DIR = Path(tempfile.gettempdir())

UPLOAD_DIR = TEMP_DIR / "test_resumes"
OUTPUT_DIR = TEMP_DIR / "output"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

app = Flask(__name__)
parser = ResumeParser()


def allowed_file(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No resume uploaded."}), 400

    file = request.files["resume"]

    if not file.filename:
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF and DOCX files are supported."}), 400

    filename = secure_filename(file.filename)
    filepath = UPLOAD_DIR / filename

    try:
        file.save(filepath)

        result = parser.parsefile(str(filepath))

        output_file = OUTPUT_DIR / f"{filepath.stem}_result.json"

        with output_file.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        return jsonify(result)

    except Exception as exc:
        return jsonify({
            "error": "Resume analysis failed.",
            "details": str(exc)
        }), 500

    finally:
        if filepath.exists():
            filepath.unlink()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
