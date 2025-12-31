# match_scorer.py

def calculate_skill_match_score(matched_skills: list, jd_skills: list) -> float:
    """
    Skill match = matched JD skills / total JD skills
    """
    if not jd_skills:
        return 0.0

    return len(matched_skills) / len(jd_skills)


def calculate_final_match_score(
    skill_score: float,
    text_similarity_score: float,
    skill_weight: float = 0.6,
    text_weight: float = 0.4
) -> dict:
    """
    Combines skill match and text similarity into a final score.
    """
    final_score = (skill_weight * skill_score) + (text_weight * text_similarity_score)

    return {
        "skill_match_percent": round(skill_score * 100, 2),
        "text_similarity_percent": round(text_similarity_score * 100, 2),
        "final_match_percent": round(final_score * 100, 2)
    }

# match_scorer.py

def calculate_final_match_score(
    skill_score: float,
    text_similarity_score: float,
    experience_score: float,
    skill_weight: float = 0.5,
    text_weight: float = 0.3,
    experience_weight: float = 0.2
) -> dict:
    """
    Combines skill, text similarity, and experience into a final score.
    Weights sum to 1.0.
    """
    final_score = (
        (skill_weight * skill_score) +
        (text_weight * text_similarity_score) +
        (experience_weight * experience_score)
    )

    return {
        "skill_match_percent": round(skill_score * 100, 2),
        "text_similarity_percent": round(text_similarity_score * 100, 2),
        "experience_match_percent": round(experience_score * 100, 2),
        "final_match_percent": round(final_score * 100, 2)
    }
