import clip
import torch
import torch.nn as nn
from PIL import Image

def load_model_platform(model_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    ckpt = torch.load(model_path, map_location=device)

    clip_model, preprocess = clip.load(ckpt["clip_model"], device=device)
    clip_model.eval()

    for p in clip_model.parameters():
        p.requires_grad = False

    classifier = nn.Linear(512, ckpt["num_classes"]).to(device)
    classifier.load_state_dict(ckpt["classifier_state"])
    classifier.eval()

    class_names = ckpt.get("class_names", None)
    return device, clip_model, classifier, preprocess, class_names

def sep_platform(image_path, device, clip_model, classifier, preprocess, class_names):
    img = preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        feat = clip_model.encode_image(img)
        feat = feat / feat.norm(dim=-1, keepdim=True)
        logits = classifier(feat)
        probs = logits.softmax(dim=-1)
    conf, idx = probs.max(dim=-1)
    if class_names:
        return {
            "label": class_names[idx.item()],
            "confidence": conf.item()
        }
    else:
        return idx.item(), conf.item()

# device, clip_model, classifier, preprocess, class_names = load_model("./separation/clip_screenshot_classifier.pt")
# # predict for vinted
# print("*-* Try for vinted : ", predict("./data/processed/train/vinted/img_0001.png", device, clip_model, classifier, preprocess, class_names))
# # predict for leboncoin
# print("*-* Try for leboncoin : ", predict("./data/processed/train/leboncoin/img_0001.png", device, clip_model, classifier, preprocess, class_names))