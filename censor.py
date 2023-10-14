import numpy as np
import torch
import clip
from PIL import Image
class Censor:
    def __init__(self, model_name="ViT-B/32", stop_words=[], device='cuda'):
        self.model, self.preprocess = clip.load(model_name)
        self.model.to(device).eval()
        self.device = device
        self.stop_words = clip.tokenize(stop_words).to(device)
        with torch.no_grad():
            self.stop_words_features = self.model.encode_text(self.stop_words).float()
            self.stop_words_features /= self.stop_words_features.norm(dim=-1, keepdim=True)
    def censor_image(self, image, t=0.25, return_sim=False):
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image_input).float()
        image_features /= image_features.norm(dim=-1, keepdim=True)
        similarity = self.stop_words_features.cpu().numpy() @ image_features.cpu().numpy().T
        if return_sim:
            return similarity
        for i in similarity:
            if i[0] > t:
                return True
        return False
    def censor_text(self, text, t=0.9, return_sim=False):
        text = clip.tokenize(text).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text).float()
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = self.stop_words_features.cpu().numpy() @ text_features.cpu().numpy().T
        if return_sim:
            return similarity
        for i in similarity:
            if i[0] > t:
                return True
        return False
