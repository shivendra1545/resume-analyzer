import re

SECTION_ALIASES = {
    "summary": {
        "professional summary", "summary", "profile", "professional profile",
        "career summary", "objective", "career objective", "about me"
    },
    "experience": {
        "experience", "work experience", "professional experience",
        "employment history", "work history", "internship", "internships"
    },
    "education": {
        "education", "academic background", "educational background",
        "academic qualifications", "qualifications"
    },
    "skills": {
        "skills", "technical skills", "technical skill", "core skills",
        "key skills", "skills & technologies", "technical expertise"
    },
    "projects": {
        "projects", "project", "academic projects", "academic project",
        "personal projects", "personal project", "key projects", "selected projects",
        "major projects", "academic & personal projects", "academic and personal projects"
    },
    "certifications": {
        "certifications", "certification", "certificates", "certificate",
        "certifications & achievements", "certification & achievements",
        "certifications and achievements", "certificates & achievements",
        "training & certifications", "licenses & certifications"
    },
    "achievements": {
        "achievements", "accomplishments", "honors", "awards",
        "hackathons & competitions", "awards & achievements"
    },
    "other": {
        "contact", "contact information", "personal information",
        "references", "interests", "hobbies"
    },
}

HEADING_TO_SECTION = {
    alias: section for section, aliases in SECTION_ALIASES.items() for alias in aliases
}


def normalize_heading(line):
    line = line.strip()
    line = re.sub(r"^[•●▪◦\-*–—]+\s*", "", line)
    line = re.sub(r"[:|]+$", "", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip().lower()


def detect_section_heading(line):
    normalized = normalize_heading(line)
    if normalized in HEADING_TO_SECTION:
        return HEADING_TO_SECTION[normalized]

    simplified = re.sub(r"[^a-z0-9& ]+", "", normalized)
    simplified = re.sub(r"\s+", " ", simplified).strip()
    if simplified in HEADING_TO_SECTION:
        return HEADING_TO_SECTION[simplified]

    # Conservative fallbacks for headings such as "ACADEMIC & PERSONAL PROJECTS".
    words = simplified.split()
    if "project" in words or "projects" in words:
        if len(words) <= 7:
            return "projects"
    if ("certification" in words or "certifications" in words
            or "certificate" in words or "certificates" in words):
        if len(words) <= 7:
            return "certifications"
    if "achievement" in words or "achievements" in words:
        if len(words) <= 7:
            return "achievements"
    return None


def clean_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?m)^\s*[•●▪◦]\s*", "- ", text)
    return text.strip()


class SectionParser:
    def __init__(self):
        self.sections = [
            "summary", "experience", "education", "skills", "projects",
            "certifications", "achievements", "other"
        ]

    def parse(self, text):
        lines = clean_text(text).splitlines()
        result = {section: [] for section in self.sections}
        current = "other"

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            detected = detect_section_heading(line)
            if detected:
                current = detected
                continue

            result[current].append(line)

        return {section: "\n".join(values).strip() for section, values in result.items()}


def parse_sections(text):
    return SectionParser().parse(text)
