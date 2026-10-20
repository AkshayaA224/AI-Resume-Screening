
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the pretrained model.
# The first run downloads the model if it is not cached.
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(resume_text, job_description):
    """Calculate semantic similarity between two text documents."""

    if not resume_text.strip() or not job_description.strip():
        raise ValueError(
            "Resume text and job description must not be empty."
        )

    embeddings = model.encode(
        [resume_text, job_description],
        normalize_embeddings=True
    )

    score = cosine_similarity(
        embeddings[0].reshape(1, -1),
        embeddings[1].reshape(1, -1)
    )[0][0]

    return float(score)


def calculate_match_percentage(resume_text, job_description):
    """Convert cosine similarity into a display percentage."""

    similarity = calculate_similarity(
        resume_text,
        job_description
    )

    # Display similarity on a 0–100 scale.
    # This is not a calibrated probability of job suitability.
    percentage = max(0.0, min(100.0, similarity * 100))

    return round(percentage, 2)
