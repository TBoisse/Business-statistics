from paddleocr import PaddleOCR
from datetime import datetime
from exchanges.transaction import Transaction

def extract_from_vinted(ocr : PaddleOCR, img_path):
    ocr_ret = ocr.predict(img_path)
    words = ocr_ret[0]["rec_texts"]
    details = []
    ret = []
    skip = False
    for i in range(len(words)):
        if skip:
            skip = False
            continue
        if "Transaction " in words[i]:
            details = []
            details.append(words[i] + " " + words[i + 1])
            skip = True
            continue
        if len(details) == 2:
            if "€" in words[i]:
                details.append(words[i])
                ret.append(Transaction(details[1], datetime.today().strftime("%d/%m/%Y"), details[0], details[2]))
            continue
        if len(details) > 0:
            details.append(words[i])
    return ret

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
