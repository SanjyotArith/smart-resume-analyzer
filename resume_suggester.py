# resume_suggester.py

def generate_resume_suggestions(results: dict):
    suggestions = []

    missing = results.get("missing_skills", [])
    skill_match = results.get("skill_match_percent", 0)
    text_similarity = results.get("text_similarity_percent", 0)
    required_exp = results.get("required_experience_years", 0)
    candidate_exp = results.get("candidate_experience_years", 0)

    # 1. Missing skills
    if missing:
        suggestions.append(
            f"Consider adding or highlighting experience with the following skills: {', '.join(missing)}."
        )

    # 2. Low skill match
    if skill_match < 50:
        suggestions.append(
            "Your skill alignment with the job description is low. Update your skills section to better reflect the required technologies."
        )

    # 3. Low text similarity
    if text_similarity < 40:
        suggestions.append(
            "Your resume wording differs significantly from the job description. Try using similar terminology and role-specific keywords."
        )

    # 4. Experience gap
    if required_exp > 0 and candidate_exp < required_exp:
        suggestions.append(
            f"The role requires at least {required_exp} years of experience. Highlight internships, projects, or hands-on work to demonstrate relevant exposure."
        )

    # 5. Strong profile
    if not suggestions:
        suggestions.append(
            "Your resume aligns well with the job description. Consider minor refinements for clarity and stronger impact."
        )

    return suggestions
