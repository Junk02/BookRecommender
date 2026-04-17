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


def compare_books(csv_path, id1, id2):
    df = pd.read_csv(csv_path)

    emb1 = df.loc[id1, "embedding"]
    emb2 = df.loc[id2, "embedding"]

    score = cosine_similarity(emb1, emb2)
    print(f"Сходство между книгами {id1} и {id2}: {score:.4f}")


if __name__ == "__main__":
    for i in range(100):
        compare_books("books_embeddings.csv", 0, i + 1)
