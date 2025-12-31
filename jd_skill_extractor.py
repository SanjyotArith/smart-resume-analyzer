# jd_skill_extractor.py

import re
from skill_normalizer import normalize_text

# Very small, GENERIC technical vocabulary anchors
TECH_KEYWORDS = [
    "java", "python", "javascript", "typescript",
    "sql", "nosql",
    "docker", "kubernetes",
    "aws", "azure", "gcp",
    "spring", "spring boot",
    "react", "angular", "vue",
    "node", "node.js",
    "rest", "rest api", "graphql",
    "microservices",
    "machine learning", "deep learning",
    "tensorflow", "pytorch",
    "ci", "cd", "jenkins",
    "linux"
]

def extract_jd_skills(jd_text: str):
    """
    Industry-style JD requirement extraction.
    Generic, role-agnostic, recruiter-clean.
    """
    jd_text = normalize_text(jd_text)

    found_skills = set()

    for keyword in TECH_KEYWORDS:
        # word-boundary match to avoid garbage phrases
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, jd_text):
            found_skills.add(keyword)

    return sorted(found_skills)


    