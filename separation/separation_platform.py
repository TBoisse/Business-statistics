from typing import Callable
import clip
import torch
import torch.nn as nn
import PIL

def load_model_platform(model_path : str):
    """
    Load the separation model (CLIP and Classifier)
    
    :param model_path: Model checkpoint.
    :type model_path: str
    """
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

def sep_platform(image_path : str, device : str, clip_model : nn.Module, classifier : nn.Linear, preprocess : Callable[[PIL.Image], torch.Tensor], class_names):
    """
    Return a platform given a screenshot.
    
    :param image_path: The screenshot path.
    :type image_path: str
    :param device: The device type to use (CPU vs GPU)
    :type device: str
    :param clip_model: The CLIP model.
    :type clip_model: nn.Module
    :param classifier: The Classifier model.
    :type classifier: nn.Linear
    :param preprocess: The preprocess function for this CLIP model.
    :type preprocess: Callable[[PIL.Image], torch.Tensor]
    :param class_names: The different class for the classifier.
    """
    img = preprocess(PIL.Image.open(image_path).convert("RGB")).unsqueeze(0).to(device)
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