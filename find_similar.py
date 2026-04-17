import pandas as pd
import numpy as np
import json


def cosine_similarity(emb1, emb2):
    if isinstance(emb1, str):
        emb1 = json.loads(emb1)
    if isinstance(emb2, str):
        emb2 = json.loads(emb2)

    v1 = np.array(emb1)
    v2 = np.array(emb2)

    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def find_similar_books(csv_path, query_embedding, top_k=10):
    """
    Получает эмбеддинг запроса и возвращает top_k ID самых похожих книг.
    """
    df = pd.read_csv(csv_path)

    similarities = []

    for idx, row in df.iterrows():
        book_emb = row["embedding"]
        score = cosine_similarity(query_embedding, book_emb)
        similarities.append((row["id"], score))

    # сортируем по убыванию
    similarities.sort(key=lambda x: x[1], reverse=True)

    # возвращаем только ID
    return [book_id for book_id, score in similarities[:top_k]]


if __name__ == "__main__":
    # пример: твой эмбеддинг запроса
    query_emb = [...]  # сюда вставляется эмбеддинг, который ты получил на бэке

    top_ids = find_similar_books("books.csv", query_emb, top_k=10)
    print(top_ids)
