from pathlib import Path
import re
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
SKILLS_FILE = BASE_DIR / "skills.csv"


def load_skill_database():
    return pd.read_csv(SKILLS_FILE)


def extract_skills(text):
    data = load_skill_database()
    found = []

    for _, row in data.iterrows():
        skill = str(row["skill"]).strip()
        aliases = str(row.get("aliases", "")).split("|")

        terms = [skill] + [a.strip() for a in aliases if a.strip()]

        for term in terms:
            pattern = r"(?<![A-Za-z0-9+#.])" + re.escape(term.lower()) + r"(?![A-Za-z0-9+#.])"
            if re.search(pattern, text.lower()):
                found.append({
                    "skill": skill,
                    "category": row["category"]
                })
                break

    unique = {}
    for item in found:
        unique[item["skill"].lower()] = item

    return list(unique.values())
