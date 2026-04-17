import pandas as pd

df = pd.read_csv("books.csv")
ids_in_csv = set(df["id"].astype(int))

print("IDs in CSV:", len(ids_in_csv))
