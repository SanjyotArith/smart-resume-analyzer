# resume_validator.py
import re

def is_likely_resume(text: str) -> bool:
    text = text.lower()

    score = 0

    # 1 Identity signals
    if re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text):
        score += 2

    if re.search(r'\b\d{10}\b|\+\d{1,3}\s?\d{6,}', text):
        score += 2

    if "linkedin.com" in text:
        score += 2

    # 2 Resume section headers
    resume_sections = [
        "experience",
        "work experience",
        "professional experience",
        "skills",
        "education",
        "projects",
        "certifications"
    ]

    for section in resume_sections:
        if section in text:
            score += 1
            break

    # 3 Job titles
    job_titles = [
        "engineer", "developer", "analyst",
        "data scientist", "intern",
        "software", "consultant"
    ]

    for title in job_titles:
        if title in text:
            score += 1
            break

    # 4 Date ranges
    if re.search(r'(20\d{2}).{0,5}(present|20\d{2})', text):
        score += 2

    #  Decision threshold
    return score >= 4

