
import re

from sklearn.metrics.pairwise import cosine_similarity

from src.skill_extractor import extract_skills, normalize_skill_name
from src.matcher import model


SEMANTIC_MATCH_THRESHOLD = 0.72
MINIMUM_SIMILARITY_MARGIN = 0.08


# Supporting phrases for selected skills.
# This list is intentionally conservative. Unknown skills still receive
# exact phrase matching when the recruiter supplies them.
SKILL_EVIDENCE = {
    "data visualization": [
        "data visualization",
        "data visualisation",
        "visualizing data",
        "visualising data",
        "visualized data",
        "visualised data",
        "visualization dashboard",
        "visualisation dashboard",
        "created charts",
        "create charts",
        "created plots",
        "created graphs",
        "matplotlib",
        "seaborn",
        "plotly",
        "tableau",
        "power bi",
        "bokeh",
        "interactive dashboard",
    ],
    "data analysis": [
        "data analysis",
        "analyze data",
        "analyse data",
        "analyzed data",
        "analysed data",
        "analyze datasets",
        "analyse datasets",
        "analyzed datasets",
        "analysed datasets",
        "exploratory data analysis",
        "eda",
        "data cleaning",
        "data preprocessing",
        "pandas",
    ],
    "statistics": [
        "statistics",
        "statistical analysis",
        "statistical methods",
        "statistical modeling",
        "statistical modelling",
        "hypothesis testing",
        "probability distributions",
        "descriptive statistics",
        "inferential statistics",
    ],
    "machine learning": [
        "machine learning",
        "trained a model",
        "trained machine learning models",
        "classification model",
        "regression model",
        "predictive model",
        "predictive modeling",
        "predictive modelling",
        "scikit-learn",
        "sklearn",
    ],
    "deep learning": [
        "deep learning",
        "neural network",
        "neural networks",
        "convolutional neural network",
        "recurrent neural network",
        "transformer model",
        "pytorch",
        "tensorflow",
    ],
    "natural language processing": [
        "natural language processing",
        "nlp",
        "text classification",
        "sentiment analysis",
        "sentiment classification",
        "named entity recognition",
        "text preprocessing",
        "tokenization",
        "tokenisation",
        "language model",
        "language models",
    ],
    "sentiment analysis": [
        "sentiment analysis",
        "sentiment classification",
        "customer review classification",
        "opinion mining",
    ],
    "generative ai": [
        "generative ai",
        "genai",
        "large language model",
        "large language models",
        "llm",
        "llms",
        "retrieval augmented generation",
        "rag pipeline",
        "prompt engineering",
    ],
    "computer vision": [
        "computer vision",
        "image classification",
        "object detection",
        "image processing",
        "opencv",
        "image segmentation",
    ],
    "sql": [
        "sql",
        "structured query language",
        "sql queries",
        "database queries",
        "joins",
    ],
    "database management": [
        "database management",
        "database administration",
        "database design",
        "database queries",
        "sql",
        "postgresql",
        "mysql",
        "sqlite",
        "mongodb",
    ],
    "autocad": [
        "autocad",
        "auto cad",
    ],
    "revit": [
        "revit",
        "autodesk revit",
    ],
    "staad.pro": [
        "staad.pro",
        "staad pro",
    ],
    "structural analysis": [
        "structural analysis",
        "structural design analysis",
        "structural engineering analysis",
    ],
    "quantity surveying": [
        "quantity surveying",
        "quantity surveyor",
    ],
    "building information modeling": [
        "building information modeling",
        "building information modelling",
        "bim",
    ],
    "solidworks": [
        "solidworks",
        "solid works",
    ],
    "mechanical engineering": [
        "mechanical engineering",
    ],
    "electrical engineering": [
        "electrical engineering",
    ],
    "communication": [
        "communication skills",
        "presented findings",
        "presentation skills",
        "communicated results",
        "technical documentation",
    ],
    "teamwork": [
        "teamwork",
        "collaborated with",
        "cross-functional team",
        "team project",
        "worked in a team",
    ],
    "problem solving": [
        "problem solving",
        "problem-solving",
        "troubleshooting",
        "root cause analysis",
        "debugging",
    ],
}


def _normalise_text(text):
    """Lowercase text and collapse repeated whitespace."""
    return re.sub(r"\s+", " ", str(text).casefold()).strip()


def _contains_phrase(text, phrase):
    """Check for a phrase with alphanumeric word boundaries."""
    text = _normalise_text(text)
    phrase = _normalise_text(phrase)

    if not text or not phrase:
        return False

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(phrase)
        + r"(?![a-z0-9])"
    )

    return re.search(pattern, text) is not None


def _has_skill_evidence(resume_text, required_skill):
    """
    Check for relevant evidence in the resume text.

    For skills without a dedicated evidence list, require the actual
    required phrase to appear in the resume. This avoids guessing.
    """
    skill = normalize_skill_name(required_skill)
    evidence_phrases = SKILL_EVIDENCE.get(skill)

    if evidence_phrases is None:
        evidence_phrases = [required_skill, skill]

    return any(
        _contains_phrase(resume_text, phrase)
        for phrase in evidence_phrases
    )


def analyze_skill_gap(
    resume_text,
    required_skills,
    semantic_threshold=SEMANTIC_MATCH_THRESHOLD,
    minimum_margin=MINIMUM_SIMILARITY_MARGIN,
):
    """
    Compare a resume against recruiter-defined required skills.

    Exact matches:
        Count toward strict coverage.

    Semantic matches:
        Suggestions that pass the configured similarity, margin,
        and resume-evidence checks. They require human review.

    Missing skills:
        Skills not detected by the current system. This does not prove
        the candidate lacks those skills.
    """
    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("Resume text must not be empty.")

    if not required_skills:
        raise ValueError("Please provide at least one required skill.")

    if not 0.0 <= semantic_threshold <= 1.0:
        raise ValueError("semantic_threshold must be between 0 and 1.")

    if not 0.0 <= minimum_margin <= 1.0:
        raise ValueError("minimum_margin must be between 0 and 1.")

    # Normalise required skills and remove duplicates.
    normalised_required = []
    required_seen = set()

    for skill in required_skills:
        if not isinstance(skill, str) or not skill.strip():
            continue

        canonical = normalize_skill_name(skill)
        key = _normalise_text(canonical)

        if key and key not in required_seen:
            required_seen.add(key)
            normalised_required.append(canonical)

    if not normalised_required:
        raise ValueError("No valid required skills were provided.")

    # Pass recruiter requirements to extraction. This is what allows
    # arbitrary skills such as STAAD.Pro to work without adding them
    # to the dictionary first.
    extracted = extract_skills(
        resume_text,
        extra_skills=normalised_required,
    )

    # Normalise extracted skills and remove duplicates.
    candidate_skills = []
    candidate_seen = set()

    for skill in extracted:
        canonical = normalize_skill_name(skill)
        key = _normalise_text(canonical)

        if key and key not in candidate_seen:
            candidate_seen.add(key)
            candidate_skills.append(canonical)

    candidate_lookup = {
        _normalise_text(skill): skill
        for skill in candidate_skills
    }

    matched_skills = []
    unmatched_required = []

    # Pass 1: exact canonical matches.
    for required in normalised_required:
        key = _normalise_text(required)

        if key in candidate_lookup:
            matched_skills.append(candidate_lookup[key])
        else:
            unmatched_required.append(required)

    missing_skills = []
    semantic_matches = []
    review_needed_skills = []

    # Pass 2: conservative semantic matching for unmatched requirements.
    if unmatched_required and candidate_skills:
        required_embeddings = model.encode(
            unmatched_required,
            normalize_embeddings=True,
        )

        candidate_embeddings = model.encode(
            candidate_skills,
            normalize_embeddings=True,
        )

        similarities = cosine_similarity(
            required_embeddings,
            candidate_embeddings,
        )

        for row_index, required in enumerate(unmatched_required):
            scores = similarities[row_index]
            ranked_indices = scores.argsort()[::-1]

            best_index = int(ranked_indices[0])
            best_score = float(scores[best_index])

            second_score = (
                float(scores[int(ranked_indices[1])])
                if len(ranked_indices) > 1
                else -1.0
            )

            margin = best_score - second_score
            best_candidate = candidate_skills[best_index]

            # Similarity alone cannot establish that the resume
            # supports a required skill.
            if not _has_skill_evidence(resume_text, required):
                missing_skills.append(required)
                continue

            if best_score < semantic_threshold:
                missing_skills.append(required)
                review_needed_skills.append({
                    "required_skill": required,
                    "reason": (
                        "Evidence found, but similarity is below "
                        "the configured threshold."
                    ),
                    "similarity": round(best_score * 100, 2),
                })
                continue

            if margin < minimum_margin:
                missing_skills.append(required)
                review_needed_skills.append({
                    "required_skill": required,
                    "reason": (
                        "Multiple candidate skills have similar scores."
                    ),
                    "similarity": round(best_score * 100, 2),
                    "margin": round(margin * 100, 2),
                })
                continue

            semantic_matches.append({
                "required_skill": required,
                "related_resume_skill": best_candidate,
                "similarity": round(best_score * 100, 2),
                "margin": round(margin * 100, 2),
                "evidence_found": True,
                "requires_human_review": True,
            })

    else:
        missing_skills.extend(unmatched_required)

    # Only exact matches contribute to strict coverage.
    total_required = len(normalised_required)

    strict_coverage = (
        len(matched_skills) / total_required * 100
        if total_required
        else 0.0
    )

    # Exploratory coverage includes semantic suggestions, but is not
    # used by the existing candidate-ranking formula.
    semantic_coverage = (
        (len(matched_skills) + len(semantic_matches))
        / total_required
        * 100
        if total_required
        else 0.0
    )

    return {
        "matched_skills": sorted(set(matched_skills)),
        "semantic_matches": semantic_matches,
        "review_needed_skills": review_needed_skills,
        "missing_skills": sorted(set(missing_skills)),
        "total_required": total_required,
        "strict_skill_coverage": round(strict_coverage, 2),
        "semantic_skill_coverage": round(semantic_coverage, 2),
        "semantic_threshold": semantic_threshold,
        "minimum_similarity_margin": minimum_margin,
    }
