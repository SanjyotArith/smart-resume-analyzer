import re
from datetime import datetime

CURRENT_DATE = datetime.now()
CURRENT_YEAR = CURRENT_DATE.year
CURRENT_MONTH = CURRENT_DATE.month

MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

def month_year_to_float(month: int, year: int) -> float:
    """Convert (month, year) → float timeline"""
    return year + (month - 1) / 12


def extract_experience_ranges(text: str):
    """
    Extracts experience date ranges from resume text.
    Supports:
    - March 2022 – March 2024
    - Jul 2023 – Present
    """
    text = text.lower()

    pattern = re.compile(
        r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})\s*[-–to]+\s*(present|current|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4})'
    )

    ranges = []

    for match in pattern.findall(text):
        start_month = MONTH_MAP[match[0]]
        start_year = int(match[1])

        start = month_year_to_float(start_month, start_year)

        if match[2] in ("present", "current"):
            end = month_year_to_float(CURRENT_MONTH, CURRENT_YEAR)
        else:
            end_parts = match[2].split()
            end_month = MONTH_MAP[end_parts[0][:3]]
            end_year = int(end_parts[1])
            end = month_year_to_float(end_month, end_year)

        if end >= start:
            ranges.append((start, end))

    return ranges


def merge_overlapping_ranges(ranges):
    """Merge overlapping experience ranges"""
    if not ranges:
        return []

    ranges.sort()
    merged = [ranges[0]]

    for current_start, current_end in ranges[1:]:
        last_start, last_end = merged[-1]

        if current_start <= last_end:
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))

    return merged


def estimate_candidate_experience(resume_text: str) -> float:
    """
    Returns total experience in years (float).
    """
    ranges = extract_experience_ranges(resume_text)
    merged_ranges = merge_overlapping_ranges(ranges)

    total_years = sum(end - start for start, end in merged_ranges)
    return round(total_years, 2)


def extract_required_experience(jd_text: str) -> int:
    """Extracts required experience from JD"""
    jd_text = jd_text.lower()
    match = re.search(r'(\d+)\s*\+?\s*years?', jd_text)
    return int(match.group(1)) if match else 0


def calculate_experience_score(candidate_years: float, required_years: int) -> float:
    """
    Normalize experience score between 0–1
    """
    if required_years <= 0:
        return 1.0

    score = candidate_years / required_years
    return min(round(score, 2), 1.0)
