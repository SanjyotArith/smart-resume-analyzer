# similarity_engine.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_text_similarity(jd_text: str, resume_text: str) -> float:
    """
    Computes semantic similarity between JD and resume using TF-IDF.
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([jd_text, resume_text])

    similarity_score = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return float(similarity_score)
