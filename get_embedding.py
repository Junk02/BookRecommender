# get_embedding.py

from sentence_transformers import SentenceTransformer
import numpy as np

# Загружаем модель один раз при импорте
model = SentenceTransformer("BAAI/bge-m3")

def get_embedding(text: str):
    """
    Получает эмбеддинг текста и возвращает его как список чисел (float).
    """
    if not isinstance(text, str) or not text.strip():
        return []

    emb = model.encode(text, normalize_embeddings=True)

    # Превращаем numpy array → обычный Python list
    return emb.tolist()
