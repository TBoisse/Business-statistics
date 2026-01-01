import os
import shutil
from PIL import Image
import pandas as pd
from tqdm import tqdm

def process_regular(csv_path, output_dir):
    df = pd.read_csv(csv_path)
    classes = df["platform"].unique()
    for cls in classes:
        os.makedirs(os.path.join(output_dir, cls), exist_ok=True)
    for i in range(len(df)):
        new_path = os.path.join(output_dir, df["platform"][i], df["image_id"][i] + "." + df["path"][i].split(".")[1])
        shutil.copy(df["path"][i], new_path)

def process_resize(csv_path, output_dir, img_size = (224,224)):
    df = pd.read_csv(csv_path)
    classes = df["platform"].unique()
    for cls in classes:
        os.makedirs(os.path.join(output_dir, cls), exist_ok=True)
        
    for _, row in tqdm(df.iterrows(), total=len(df)):
        src_path = row["path"]
        cls = row["platform"]
        img_id = row["image_id"]

        try:
            img = Image.open(src_path).convert("RGB")
            img = img.resize(img_size)
            dst_path = os.path.join(output_dir, cls, f"{img_id}.png")
            img.save(dst_path)
        except Exception as e:
            print(f"Erreur {src_path}: {e}")

def process_reset(output_dir):
    for path in os.listdir(output_dir):
        full_path = os.path.join(output_dir, path)
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            os.remove(full_path)

csv_path = "data/metadata/annotations.csv"
output_dir = "data/processed"
# process_reset(output_dir)
# process_resize(csv_path, output_dir)
# process_regular(csv_path, output_dir)
