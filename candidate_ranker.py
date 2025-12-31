# candidate_ranker.py

from jd_skill_extractor import extract_jd_skills
from resume_skill_extractor import extract_resume_skills
from similarity_engine import compute_text_similarity
from match_scorer import calculate_skill_match_score, calculate_final_match_score
from experience_extractor import (
    extract_required_experience,
    estimate_candidate_experience,
    calculate_experience_score
)

def rank_candidates(jd_text: str, resumes: list):
    """
    Ranks multiple candidates against a single JD.

    resumes: list of dicts
    [
        {
            "candidate_name": "Alice",
            "resume_text": "...."
        },
        ...
    ]
    """

    jd_skills = extract_jd_skills(jd_text)
    required_years = extract_required_experience(jd_text)

    ranked_results = []

    for resume in resumes:
        resume_text = resume["resume_text"]
        candidate_name = resume["candidate_name"]

        # Skill matching
        skill_result = extract_resume_skills(resume_text, jd_skills)
        skill_score = calculate_skill_match_score(
            skill_result["matched"],
            jd_skills
        )

        # Text similarity
        text_similarity = compute_text_similarity(jd_text, resume_text)

        # Experience
        candidate_years = estimate_candidate_experience(resume_text)
        experience_score = calculate_experience_score(
            candidate_years,
            required_years
        )

        # Final score
        final_scores = calculate_final_match_score(
            skill_score,
            text_similarity,
            experience_score
        )

        ranked_results.append({
            "candidate_name": candidate_name,
            "final_score": final_scores["final_match_percent"],
            "skill_match_percent": final_scores["skill_match_percent"],
            "text_similarity_percent": final_scores["text_similarity_percent"],
            "experience_match_percent": final_scores["experience_match_percent"],
            "matched_skills": skill_result["matched"],
            "missing_skills": skill_result["missing"],
            "estimated_experience_years": candidate_years
        })

    # Sort candidates by final score (descending)
    ranked_results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return ranked_results
