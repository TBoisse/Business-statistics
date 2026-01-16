from paddleocr import PaddleOCR
from datetime import datetime
from exchanges.transaction import Transaction

def extract_from_vinted(ocr : PaddleOCR, img_path, tr_type = "unknown", date = ""):
    ocr_ret = ocr.predict(img_path)
    words = ocr_ret[0]["rec_texts"]
    details = []
    ret = []
    step = 0
    title = ""
    skip = 0
    if len(date) == 0:
        date = datetime.today().strftime("%d/%m/%Y")
    for i in range(len(words)):
        if skip > 0:
            skip -= 1
            continue
        if words[i] == "Finalisées":
            step = 1
            continue
        if step == 0:
            continue
        if "Commande" in words[i] or "Transaction" in words[i]:
            if step == 3:
                details.append(words[i] + " " + words[i + 1])
                ret.append(Transaction(details[0], date, details[2], details[1], tr_type))
            details = []
            title = ""
            skip = 1
            step = 1
            continue
        if "€" in words[i]:
            if step == 1:
                details = []
                title = ""
                skip = 2
                continue
            else:
                step = 3
                details.append(title[:-1])
                details.append(float(words[i].split(" ")[0].replace(",",".")))
                continue
        step = 2
        title += words[i]
        title += " "
    return ret

def extract_from_leboncoin(ocr : PaddleOCR, img_path : str, tr_type = "unknown"):
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
                details.append(float(word.split(" ")[0].replace(",",".")))
                ret.append(Transaction(details[2], details[0], details[1], details[3], tr_type))
            continue
        if len(details) > 0:
            details.append(word)
    return ret
