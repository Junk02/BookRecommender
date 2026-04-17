import os
import pandas as pd

COVERS_DIR = "booksite/public/covers"

df = pd.read_csv("books.csv")
valid_ids = set(df["id"].astype(int))

for fname in os.listdir(COVERS_DIR):
    if not fname.startswith("book_"):
        continue

    try:
        num = int(fname.split("_")[1].split(".")[0])
    except:
        continue

    if num not in valid_ids:
        print("[DELETE]", fname)
        os.remove(os.path.join(COVERS_DIR, fname))
