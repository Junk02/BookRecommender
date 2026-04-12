# import kaggle
#
# kaggle.api.dataset_download_files(
#     'sharthz23/mts-library',
#     path='mts_dataset',
#     unzip=True
# )
#
# print("Готово!")

import pandas as pd
from labirinth_parser import get_book_description





items = pd.read_csv("mts_dataset/items.csv")

# INIT

items_dict = {row["id"]: row for _, row in items.iterrows()}


desc = get_book_description("Посторонний", "Альбер Камю")
print(desc)
