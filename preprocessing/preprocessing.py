import os
from PIL import Image
import pandas as pd
from tqdm import tqdm

csv_path = "data/metadata/annotations.csv"
output_dir = "data/processed"
img_size = (224, 224)  # CLIP ViT-B/32

# splits = ["train", "val", "test"]
splits = ["train"]
classes = ["leboncoin", "vinted"]

for split in splits:
    for cls in classes:
        os.makedirs(os.path.join(output_dir, split, cls), exist_ok=True)

df = pd.read_csv(csv_path)

for _, row in tqdm(df.iterrows(), total=len(df)):
    src_path = row["path"]
    # split = row["split"]
    split = splits[0]
    cls = row["platform"]
    img_id = row["image_id"]

    try:
        img = Image.open(src_path).convert("RGB")
        img = img.resize(img_size)
        dst_path = os.path.join(output_dir, split, cls, f"{img_id}.png")
        img.save(dst_path)
    except Exception as e:
        print(f"Erreur {src_path}: {e}")
