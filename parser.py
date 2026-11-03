from text_extractor import extract_text_from_file
from section_parser import SectionParser, clean_text
from information_extractor import extract_contact_information
from skill_extractor import extract_skills
from ner_extractor import NERExtractor


class ResumeParser:
    def __init__(self):
        self.ner = NERExtractor()
        self.section_parser = SectionParser()

    def parse_file(self, filepath):
        # 1. Extract text from PDF/DOCX
        raw_text = extract_text_from_file(filepath)

        # 2. Clean extracted text
        cleaned_text = clean_text(raw_text)

        # 3. Extract contact information
        contact = extract_contact_information(cleaned_text)

        # 4. Detect resume sections
        sections = self.section_parser.parse(cleaned_text)

        # 5. Extract skills using skills.csv
        skills = extract_skills(cleaned_text)

        # 6. Extract entities and candidate name
        ner = self.ner.extract(cleaned_text)

        candidate_name = ner.get("name")

        filename = filepath.replace("\\", "/").split("/")[-1]

        return {
            "file": filename,

            "candidate": {
                "name": candidate_name,
                "email": (
                    contact["emails"][0]
                    if contact["emails"]
                    else None
                ),
                "phone": (
                    contact["phones"][0]
                    if contact["phones"]
                    else None
                ),
                "linkedin": (
                    contact["linkedin"][0]
                    if contact["linkedin"]
                    else None
                ),
                "portfolio_or_github": (
                    contact["portfolio_or_github"][0]
                    if contact["portfolio_or_github"]
                    else None
                )
            },

            "contact": contact,

            "skills": skills,

            "entities": ner.get("entities", []),

            "organizations": ner.get("organizations", []),

            "sections": sections,

            "raw_text": raw_text
        }

    # PDF requirement compatibility
    def parsefile(self, filepath):
        return self.parse_file(filepath)