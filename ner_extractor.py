import re
import spacy


class NERExtractor:

    def __init__(self, model_name="en_core_web_sm"):
        self.nlp = spacy.load(model_name)

    @staticmethod
    def _clean_line(line):
        return re.sub(r"\s+", " ", line).strip(" |•\t\r\n")

    @staticmethod
    def _is_heading(line):
        headings = {
            "resume", "cv", "profile", "summary", "education",
            "experience", "skills", "projects", "certifications",
            "achievements", "contact", "interests", "hobbies"
        }
        return line.lower().strip().rstrip(":") in headings

    @staticmethod
    def _is_contact_line(line):
        low = line.lower()
        return (
            "@" in line or
            "linkedin.com" in low or
            "github.com" in low or
            bool(re.search(r"\+?\d[\d\s().-]{8,}\d", line))
        )

    def _find_header_name(self, text):
        match = re.search(
            r"\b([A-Z]{3,20})\b(?=COMPUTER SCIENCE|COMPUTER|STUDENT)",
            text
        )

        if match:
            return match.group(1).title()

        lines = [
            self._clean_line(x)
            for x in text.splitlines()
            if x.strip()
        ]

        blocked = {
            "resume", "profile", "summary", "student",
            "developer", "engineer", "computer", "science",
            "skills", "languages"
        }

        for line in lines[:25]:
            if self._is_heading(line) or self._is_contact_line(line):
                continue

            words = re.findall(r"[A-Za-z][A-Za-z.'-]*", line)

            if len(words) == 1 and words[0].isupper():
                if words[0].lower() not in blocked:
                    return words[0].title()

            if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words):
                if not any(w.lower() in blocked for w in words):
                    return line

        return None

    def extract(self, text):
        doc = self.nlp(text)

        entities = []
        organizations = []

        for ent in doc.ents:
            value = ent.text.strip()

            if not value:
                continue

            entities.append({
                "text": value,
                "label": ent.label_
            })

            if ent.label_ in {"ORG", "GPE", "FAC"}:
                organizations.append(value)

        return {
            "name": self._find_header_name(text),
            "entities": entities,
            "organizations": list(dict.fromkeys(organizations))
        }