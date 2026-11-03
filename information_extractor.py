import re


EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

PHONE_PATTERNS = [
    r"(?<!\d)(?:\+91[\s.-]?)?[6-9]\d{9}(?!\d)",
    r"(?<!\d)(?:\+91[\s.-]?)?\d{3}[\s.-]\d{3}[\s.-]\d{4}(?!\d)"
]

URL_PATTERN = r"(?:https?://|www\.)[^\s<>()]+"

LINKEDIN_PATTERN = r"(?:https?://)?(?:www\.)?linkedin\.com/[^\s<>()]+"
PORTFOLIO_PATTERN = r"(?:https?://)?(?:www\.)?[^\s<>()]*(?:github\.com|gitlab\.com|portfolio)[^\s<>()]*"


def unique_clean(values):
    cleaned = []
    seen = set()

    for value in values:
        value = value.strip().rstrip(".,;")
        if value and value.lower() not in seen:
            cleaned.append(value)
            seen.add(value.lower())

    return cleaned


def extract_emails(text):
    emails = re.findall(EMAIL_PATTERN, text)

    cleaned_emails = []

    for email in emails:
        email = re.sub(r"(?i)(email|address)$", "", email)
        cleaned_emails.append(email)

    return unique_clean(cleaned_emails)


def extract_phones(text):
    matches = []

    for pattern in PHONE_PATTERNS:
        matches.extend(re.findall(pattern, text))

    merged_phone = re.findall(r"(?<!\d)[6-9]\d{8,9}(?!\d)", text)
    matches.extend(merged_phone)

    return unique_clean(matches)


def extract_urls(text):
    return unique_clean(re.findall(URL_PATTERN, text))


def extract_linkedin(text):
    return unique_clean(re.findall(LINKEDIN_PATTERN, text, flags=re.IGNORECASE))


def extract_portfolio_links(text):
    return unique_clean(re.findall(PORTFOLIO_PATTERN, text, flags=re.IGNORECASE))


def extract_contact_information(text):
    return {
        "emails": extract_emails(text),
        "phones": extract_phones(text),
        "linkedin": extract_linkedin(text),
        "portfolio_or_github": extract_portfolio_links(text),
        "all_urls": extract_urls(text)
    }
