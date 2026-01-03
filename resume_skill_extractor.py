from skill_mapper import SkillMapper, extract_phrases

mapper = SkillMapper()

def extract_resume_skills(resume_text: str, jd_skills: list):
    phrases = extract_phrases(resume_text)

    resume_skills = set()
    for phrase in phrases:
        skill_id, score = mapper.map_phrase(phrase)
        if skill_id:
            resume_skills.add(skill_id)

    matched = sorted(set(jd_skills) & resume_skills)
    missing = sorted(set(jd_skills) - resume_skills)

    return {
        "matched": matched,
        "missing": missing
    }
