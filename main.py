from paddleocr import PaddleOCR
import os
import pandas as pd
from exchanges import extract_from_leboncoin, extract_from_vinted, initiate_transaction, write_transaction
from separation import load_model, predict_platform

input_dir = "data/raw"
csv_path = "statistics.csv"
ocr = PaddleOCR(lang="fr")
device, clip_model, classifier, preprocess, class_names = load_model("separation/clip_screenshot_classifier.pt")

initiate_transaction(csv_path)
with open(csv_path, "a") as f:
    for file in os.listdir(input_dir):
        path = os.path.join(input_dir, file)
        platform = predict_platform(path, device, clip_model, classifier, preprocess, class_names)["label"]
        print(file, platform)
        if platform == "vinted":
            transactions = extract_from_vinted(ocr, path)
        else:
            transactions = extract_from_leboncoin(ocr, path)
        write_transaction(f, transactions)

df = pd.read_csv(csv_path, sep=";")
df["date"] = pd.to_datetime(df["date"],dayfirst=True,format="mixed")
df.sort_values(by="date", inplace=True, ascending=False)
df.to_csv(csv_path, sep=";", index=False)