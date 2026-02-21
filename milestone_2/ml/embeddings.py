from sentence_transformers import SentenceTransformer
import numpy as np

# lightweight & fast model (perfect for hackathon)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> np.ndarray:
    """
    Convert ticket text into semantic vector.
    """
    return model.encode(text)


def cosine_similarity(vec1, vec2) -> float:
    """
    Compute cosine similarity between two vectors.
    Returns value between -1 and 1.
    """
    return float(np.dot(vec1, vec2) /
                 (np.linalg.norm(vec1) * np.linalg.norm(vec2)))