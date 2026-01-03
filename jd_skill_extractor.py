from skill_mapper import SkillMapper, extract_phrases

mapper = SkillMapper()

def extract_skills_from_jd(jd_text: str):
    phrases = extract_phrases(jd_text)

    skills = set()
    for phrase in phrases:
        skill_id, score = mapper.map_phrase(phrase)
        if skill_id:
            skills.add(skill_id)

    return sorted(skills)
