from pathlib import Path
import json
from parser import ResumeParser


BASE_DIR = Path(__file__).resolve().parent
RESUME_DIR = BASE_DIR / "test_resumes"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


def find_first_resume():
    supported = {".pdf", ".docx"}

    for file in sorted(RESUME_DIR.iterdir()):
        if file.is_file() and file.suffix.lower() in supported:
            return file

    return None


resume = find_first_resume()

if resume is None:
    print("No resume found.")
    print("Put a PDF or DOCX file inside: test_resumes/")
    raise SystemExit(1)

parser = ResumeParser()
result = parser.parsefile(str(resume))

output_file = OUTPUT_DIR / f"{resume.stem}_result.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(result, file, indent=4, ensure_ascii=False)

print(f"Resume: {resume.name}")
print(f"JSON saved to: {output_file}")
print(json.dumps(result, indent=4, ensure_ascii=False))
