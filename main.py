from paddleocr import PaddleOCR
import pandas as pd
from exchanges.statistics import extract_from_leboncoin 
from exchanges.transaction import write_transaction

ocr = PaddleOCR(lang="fr")

with open("statistics.csv", "a") as f:
    for i in range(1,6):
        path = f"data/raw/leboncoin/img_000{i}.jpeg"
        transactions = extract_from_leboncoin(ocr, path)
        write_transaction(f, transactions)

df = pd.read_csv("statistics.csv", sep=";")
df["date"] = pd.to_datetime(df["date"],dayfirst=True,format="mixed")
df.sort_values(by="date", inplace=True, ascending=False)
df.to_csv("statistics.csv", sep=";", index=False)