import argparse
import os
import pandas as pd
from paddleocr import PaddleOCR
from preprocessing import process_reset, process_regular
from exchanges import extract_from_leboncoin, extract_from_vinted, initiate_transaction, write_transaction
from separation import load_model_platform, sep_platform, sep_buysell

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Compute Statistics',
                    description='This program has 2 main uses : launching the preprocessing for the raw data and computing statistics.',
                    epilog='Don\'t hesitate to report any issue encountered')
    parser.add_argument('-r', '--reset', action='store_true', help="When set, reset the folder './data/processed'.")
    parser.add_argument('-p', '--preprocessing', action='store_true', help="When set, produces preprocessing using the './data/processed' folder.")
    parser.add_argument('-o', '--output_path', default="statistics.csv", help="Select where will the statistics be stored.")
    parser.add_argument('-n', '--no_statistics', action='store_true', help="When set, stops before producing statistics. Mainly useful when only preprocessing is wanted.")
    args = parser.parse_args()
    if not os.path.isfile(args.output_path):
        initiate_transaction(args.output_path)
    input_dir = "data/real"
    tmp_path = "temporary.csv"
    annotation_preprocessing_path = "data/metadata/annotations_training.csv"
    annotation_real_path = "data/metadata/annotations_real.csv"
    processed_dir = "data/processed"
    model_path = "separation/clip_screenshot_classifier.pt"

    if args.reset:
        process_reset(processed_dir)
    if args.preprocessing:
        process_regular(annotation_preprocessing_path, processed_dir)
    if args.no_statistics:
        quit()

    ocr = PaddleOCR(lang="fr")
    device, clip_model, classifier, preprocess, class_names = load_model_platform(model_path)
    df_annotations = pd.read_csv(annotation_real_path, sep=",")

    initiate_transaction(tmp_path)
    with open(tmp_path, "a") as f:
        for file in os.listdir(input_dir):
            path = os.path.join(input_dir, file)
            platform = sep_platform(path, device, clip_model, classifier, preprocess, class_names)["label"]
            tr_type = sep_buysell(path, platform)
            if platform == "vinted":
                date = df_annotations[df_annotations["image_id"] == file.split(".")[0]]["date"].values[0]
                print(file, platform, tr_type, date)
                transactions = extract_from_vinted(ocr, path, tr_type=tr_type, date=date)
            else:
                transactions = extract_from_leboncoin(ocr, path, tr_type)
            write_transaction(f, transactions)

    df_tmp = pd.read_csv(tmp_path, sep=";")
    df_real = pd.read_csv(args.output_path, sep=";")
    df = pd.concat([df_tmp, df_real])
    df["date"] = pd.to_datetime(df["date"],dayfirst=True,format="mixed")
    df = df.sort_values(by="date", ascending=False)
    df = df.drop_duplicates(subset=["title", "price"])
    df.to_csv(args.output_path, sep=";", index=False)
    os.remove(tmp_path)