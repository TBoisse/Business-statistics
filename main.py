from paddleocr import PaddleOCR
import os
import pandas as pd
import cv2
from exchanges import extract_from_leboncoin, extract_from_vinted, initiate_transaction, write_transaction
from separation import load_model_platform, sep_platform, sep_buysell

input_dir = "data/raw"
csv_path = "statistics.csv"
ocr = PaddleOCR(lang="fr")
device, clip_model, classifier, preprocess, class_names = load_model_platform("separation/clip_screenshot_classifier.pt")

initiate_transaction(csv_path)
with open(csv_path, "a") as f:
    for file in os.listdir(input_dir):
        path = os.path.join(input_dir, file)
        platform = sep_platform(path, device, clip_model, classifier, preprocess, class_names)["label"]
        tr_type = sep_buysell(path, platform)
        print(file, platform, tr_type)
        if platform == "vinted":
            transactions = extract_from_vinted(ocr, path, tr_type)
        else:
            transactions = extract_from_leboncoin(ocr, path, tr_type)
        write_transaction(f, transactions)

df = pd.read_csv(csv_path, sep=";")
df["date"] = pd.to_datetime(df["date"],dayfirst=True,format="mixed")
df.sort_values(by="date", inplace=True, ascending=False)
df.to_csv(csv_path, sep=";", index=False)