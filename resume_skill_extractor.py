# resume_skill_extractor.py

from skill_normalizer import normalize_text

def extract_resume_skills(resume_text: str, jd_skills: list):
    """
    Checks which JD-defined skills are present in the resume.
    """
    resume_text = normalize_text(resume_text)

    matched_skills = []
    missing_skills = []

    for skill in jd_skills:
        if skill in resume_text:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "matched": sorted(set(matched_skills)),
        "missing": sorted(set(missing_skills))
    }
