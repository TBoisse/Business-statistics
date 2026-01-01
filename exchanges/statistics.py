from paddleocr import PaddleOCR
import pandas as pd
from exchanges.transaction import Transaction

def extract_from_vinted(ocr : PaddleOCR, img_path):

    return

def extract_from_leboncoin(ocr : PaddleOCR, img_path : str):
    ocr_ret = ocr.predict(img_path)
    details = []
    ret = []
    for word in ocr_ret[0]["rec_texts"]:
        if "Vente du" in word:
            details = []
            details.append(word.split("Vente du ")[1])
            continue
        if len(details) == 3:
            if "€" in word:
                details.append(word)
                ret.append(Transaction(details[2], details[0], details[1], details[3]))
            continue
        if len(details) > 0:
            details.append(word)
    return ret
