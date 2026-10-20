
from src.matcher import calculate_similarity
from src.skill_gap import analyze_skill_gap


def rank_candidate(
    resume_text,
    job_description,
    required_skills,
    semantic_weight=0.70,
    skill_weight=0.30,
):
    """Calculate a configurable candidate ranking score."""

    if not 0 <= semantic_weight <= 1:
        raise ValueError("Semantic weight must be between 0 and 1.")

    if not 0 <= skill_weight <= 1:
        raise ValueError("Skill weight must be between 0 and 1.")

    if abs(semantic_weight + skill_weight - 1.0) > 1e-9:
        raise ValueError("The weights must sum to 1.")

    # Semantic similarity between resume and job description.
    similarity = calculate_similarity(
        resume_text, job_description
    )

    # Convert to a display percentage, bounded to 0–100.
    semantic_score = max(0.0, min(100.0, similarity * 100))

    # Explicit skill coverage from our skill-gap module.
    gap = analyze_skill_gap(resume_text, required_skills)
    skill_coverage = gap["strict_skill_coverage"]

    # Combined score used for preliminary ranking.
    ranking_score = (
        semantic_weight * semantic_score
        + skill_weight * skill_coverage
    )

    return {
        "semantic_similarity": round(semantic_score, 2),
        "skill_coverage": round(skill_coverage, 2),
        "ranking_score": round(ranking_score, 2),
        "skill_gap": gap,
    }
