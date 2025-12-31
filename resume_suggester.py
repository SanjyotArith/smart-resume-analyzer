# resume_suggester.py

def generate_resume_suggestions(
    missing_skills: list,
    experience_score: float,
    text_similarity_score: float,
    required_experience: int,
    candidate_experience: float
):
    """
    Generates actionable resume improvement suggestions.
    Deterministic, explainable, recruiter-safe.
    """

    suggestions = []

    # 1. Missing skills suggestions
    if missing_skills:
        suggestions.append(
            "Consider adding or highlighting experience with the following skills: "
            + ", ".join(missing_skills) + "."
        )

    # 2. Experience-related suggestions
    if required_experience > 0 and candidate_experience < required_experience:
        suggestions.append(
            f"The job requires at least {required_experience} years of experience. "
            "Consider clearly highlighting internships, projects, or relevant work "
            "that demonstrate hands-on experience."
        )

    # 3. Resume–JD alignment suggestions
    if text_similarity_score < 0.6:
        suggestions.append(
            "Your resume wording differs from the job description. "
            "Consider aligning terminology and responsibilities more closely "
            "with the job requirements."
        )

    # 4. Positive reinforcement (important)
    if not suggestions:
        suggestions.append(
            "Your resume aligns well with the job description. "
            "Ensure key achievements and responsibilities are clearly described."
        )

    return suggestions
