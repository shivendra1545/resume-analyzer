# Automated Resume Analyzer for Job Portals

## Project Scope

This project implements the PDF-specified core resume analyzer:

1. PDF/DOCX document ingestion
2. Text extraction
3. Text cleaning
4. Section segmentation
5. Regex-based contact extraction
6. spaCy NER
7. Skill knowledge base and skill extraction
8. Structured JSON output
9. Flask API wrapper
10. Basic browser upload interface
11. Local resume testing
12. Documentation

## Folder Structure

```text
Automated-Resume-Analyzer/
├── app.py
├── parser.py
├── text_extractor.py
├── section_parser.py
├── information_extractor.py
├── skill_extractor.py
├── ner_extractor.py
├── skill.csv / skills.csv
├── requirements.txt
├── README.md
├── test_parser.py
├── test_resumes/
├── output/
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Installation

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## How to Store a Resume

Create/use:

```text
test_resumes/
```

Put your test resume inside it:

```text
test_resumes/
└── Prashant_Resume.pdf
```

or:

```text
test_resumes/
└── Prashant_Resume.docx
```

The filename can be anything.

## Test the Parser Directly

```powershell
python test_parser.py
```

The generated structured result is saved in:

```text
output/
```

Example:

```text
output/
└── Prashant_Resume_result.json
```

## Run the Flask Application

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Choose your PDF/DOCX resume and click:

```text
Analyze Resume
```

The uploaded file is stored in `test_resumes/` and the JSON result is stored in `output/`.

## Important Limitation

This implementation extracts text from normal text-based PDF files. A scanned/image-only PDF may not contain machine-readable text and would require OCR, which is outside the supplied project brief.

## NER Note

The spaCy `en_core_web_sm` model provides general named-entity recognition. University and degree extraction may depend on the wording and layout of a particular resume. The project therefore combines NER with section-based parsing rather than claiming that a generic NER model perfectly identifies every resume field.

## Final Testing

The supplied project specification asks for testing across 10–20 different resume layouts. For that test, place multiple PDF/DOCX files in `test_resumes/` and run the parser against each file.

## Deliverables

- Parser engine: `parser.py`
- Skill knowledge base: `skills.csv`
- API wrapper: `app.py`
- Documentation: `README.md`
- Test data folder: `test_resumes/`
- Structured results: `output/`
