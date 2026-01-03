import jd_skill_extractor
import resume_skill_extractor
import similarity_engine
import experience_extractor
from resume_suggester import generate_resume_suggestions



def analyze_job_seeker(jd_text, raw_resume_text, cleaned_resume_text):
    """
    Core analysis engine.
    - RAW resume text is used ONLY for experience extraction
    - CLEANED resume text is used for skills & similarity
    """

    # -----------------------------
    # 1. Skill extraction (JD)
    # -----------------------------
    jd_skills = jd_skill_extractor.extract_skills_from_jd(jd_text)

    skill_result = resume_skill_extractor.extract_resume_skills(
        cleaned_resume_text,
        jd_skills
    )

    matched_skills = skill_result["matched"]
    missing_skills = skill_result["missing"]

    skill_match_percent = round(
        (len(matched_skills) / max(len(jd_skills), 1)) * 100,
        2
    )

    # -----------------------------
    # 2. Text similarity (CLEANED)
    # -----------------------------
    text_similarity_percent = round(
        similarity_engine.compute_text_similarity(
            jd_text,
            cleaned_resume_text
        ) * 100,
        2
    )

    # -----------------------------
    # 3. Experience analysis (RAW)
    # -----------------------------
    required_years = experience_extractor.extract_required_experience(jd_text)
    candidate_years = experience_extractor.estimate_candidate_experience(
        raw_resume_text
    )

    experience_match_percent = (
        experience_extractor.calculate_experience_score(
            candidate_years,
            required_years
        ) * 100
    )

    # Experience eligibility (ATS-style)
    if required_years > 0:
        experience_pass = candidate_years >= required_years
    else:
        experience_pass = None

    # -----------------------------
    # 4. Final weighted score
    # -----------------------------
    final_match_percent = round(
        0.5 * skill_match_percent +
        0.3 * text_similarity_percent +
        0.2 * experience_match_percent,
        2
    )

    # -----------------------------
    # 5. Resume improvement suggestions
    # -----------------------------
    results_snapshot = {
        "missing_skills": missing_skills,
        "skill_match_percent": skill_match_percent,
        "text_similarity_percent": text_similarity_percent,
        "required_experience_years": required_years,
        "candidate_experience_years": candidate_years
    }

    suggestions = generate_resume_suggestions(results_snapshot)


    # -----------------------------
    # 6. Return structured result
    # -----------------------------
    return {
        "final_match_percent": final_match_percent,
        "skill_match_percent": skill_match_percent,
        "text_similarity_percent": text_similarity_percent,
        "experience_match_percent": experience_match_percent,

        "matched_skills": matched_skills,
        "missing_skills": missing_skills,

        "candidate_experience_years": candidate_years,
        "required_experience_years": required_years,
        "experience_pass": experience_pass,
        "suggestions": suggestions

    }
