# experience_extractor.py

import re
from datetime import datetime

CURRENT_YEAR = datetime.now().year


def extract_required_experience(jd_text: str) -> int:
    """
    Extracts minimum required experience from JD.
    Examples:
      '2+ years', '3 years', 'minimum 5 years'
    Returns integer years. Defaults to 0 if not found.
    """
    jd_text = jd_text.lower()

    patterns = [
        r'(\d+)\s*\+\s*years',
        r'(\d+)\s*years',
        r'minimum\s*(\d+)\s*years'
    ]

    for pattern in patterns:
        match = re.search(pattern, jd_text)
        if match:
            return int(match.group(1))

    return 0


def estimate_candidate_experience(resume_text: str) -> float:
    """
    Estimates candidate experience in years using date ranges.
    Looks for patterns like:
      2020-2024
      2019 – 2023
    Falls back to explicit 'X years' if found.
    """
    resume_text = resume_text.lower()

    # 1) Explicit years mentioned (e.g., '3 years of experience')
    explicit = re.search(r'(\d+)\s*years', resume_text)
    if explicit:
        return float(explicit.group(1))

    # 2) Date ranges (e.g., 2020-2024)
    ranges = re.findall(r'(20\d{2})\s*[-–]\s*(20\d{2})', resume_text)
    if ranges:
        total_years = 0
        for start, end in ranges:
            start, end = int(start), int(end)
            if end >= start:
                total_years += (end - start)
        if total_years > 0:
            return float(total_years)

    return 0.0


def calculate_experience_score(candidate_years: float, required_years: int) -> float:
    """
    Converts experience comparison to a normalized score [0, 1].
    - Below requirement → proportional penalty
    - Meets/exceeds requirement → capped at 1.0
    """
    if required_years <= 0:
        return 1.0  # no requirement → no penalty

    score = candidate_years / required_years
    return min(round(score, 2), 1.0)
