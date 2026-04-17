from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")  # или другая модель

text = """Жанр: биография. Темы: жизнь, творчество, литература. 
Смысл: Книга представляет собой биографический очерк о жизни и творчестве Сергея Есенина."""

emb = model.encode(text, normalize_embeddings=True)  # emb — вектор (numpy array)
print(emb.shape)  # например (1024,)
print(emb)
