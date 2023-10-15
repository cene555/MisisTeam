N_CORES = 128 # Где N_CORES - количество ядер CPU

import os

os.environ["MKL_NUM_THREADS"] = str(N_CORES)

os.environ["NUMEXPR_NUM_THREADS"] = str(N_CORES)

os.environ["OMP_NUM_THREADS"] = str(N_CORES)
import sys
from diffusers import KandinskyV22PriorPipeline, KandinskyV22Pipeline, KandinskyV22PriorEmb2EmbPipeline, KandinskyV22ControlnetImg2ImgPipeline, KandinskyV22Img2ImgPipeline
import torch
from PIL import Image
from PIL import ImageDraw, ImageFont
from copy import deepcopy
from deep_translator import GoogleTranslator

from rembg import remove
from diffusers import KandinskyV22PriorEmb2EmbPipeline
from diffusers import KandinskyV22ControlnetImg2ImgPipeline
import torch
import PIL
import torch
from diffusers.utils import load_image
from torchvision import transforms
from transformers import CLIPVisionModelWithProjection
from diffusers.models import UNet2DConditionModel
import numpy as np
import imageio.v3 as iio

#from deforum_kandinsky import DeforumKandinsky
#decoder2 = KandinskyV22Img2ImgPipeline.from_pretrained('kandinsky-community/kandinsky-2-2-decoder', torch_dtype=torch.float16).to('cuda')

decoder = KandinskyV22Img2ImgPipeline.from_pretrained('kandinsky-community/kandinsky-2-2-decoder', torch_dtype=torch.float16).to('cuda')
prior = KandinskyV22PriorPipeline.from_pretrained('kandinsky-community/kandinsky-2-2-prior', torch_dtype=torch.float16).to('cuda')

prompt = 'pizza in the space, photo'
def prepare_caption(caption): return GoogleTranslator(source='ru', target='en').translate(caption)

def delete_bg(img, img2):
    min_size = min(img2.size[0], img2.size[1])

    img = img.resize((min_size, min_size))
    img = np.array(img)
    img2 = np.array(img2)
    output = remove(img)
    m = 0
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            m = max(output[i][j][3], m)
            if output[i][j][3] >= 80:
                img2[i][j] = output[i][j][:3]
    return Image.fromarray(img2)

def generate_avatar(decoder, prior, prompt, text=None, style_image=None, face_image=None, animation=None):
    print('face_image', face_image, 'style_image', style_image)
    prompt = prepare_caption(prompt)
    zero_img = PIL.Image.new(mode="RGB", size=(200, 200))
    img_emb = prior(prompt=prompt, num_inference_steps=50, num_images_per_prompt=1, guidance_scale=1.0).image_embeds
    if style_image is not None:
        img_emb2 = prior.interpolate(images_and_prompts=[style_image], weights=[1.0], num_inference_steps=25, num_images_per_prompt=1, guidance_scale=4.0).image_embeds
        img_emb = img_emb * 0.55 + img_emb2 * 0.45
    negative_emb = prior(prompt='blow quility', num_inference_steps=25, num_images_per_prompt=1, guidance_scale=4.0)
    images = decoder(image=zero_img, strength=1.0, image_embeds=img_emb, negative_image_embeds=negative_emb.negative_image_embeds, num_inference_steps=100, height=832, width=832, guidance_scale=4.0).images
    if face_image is not None:
        images[0] = delete_bg(face_image, images[0])
    if text is not None:
        img = deepcopy(images[0])
        W, H = img.size
        myFont = ImageFont.truetype('DejaVuSansCondensed.ttf', 40)

        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), text, font=myFont)
        draw.text(((W-w)/2, 25), text, font=myFont, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        return img
    else:
        return images[0]

    
def generate_preview(decoder, prior, prompt, text=None, style_image=None, face_image=None, animation=None):
    prompt = prepare_caption(prompt)
    prompt = '4k photo of ' + prompt
    zero_img = PIL.Image.new(mode="RGB", size=(200, 200))
    img_emb = prior(prompt=prompt, num_inference_steps=50, num_images_per_prompt=1, guidance_scale=1.5).image_embeds
    if style_image is not None:
        img_emb2 = prior.interpolate(images_and_prompts=[style_image], weights=[1.0], num_inference_steps=25, num_images_per_prompt=1, guidance_scale=4.0).image_embeds
        img_emb = img_emb * 0.75 + img_emb2 * 0.25
    negative_emb = prior(prompt='blow quility', num_inference_steps=25, num_images_per_prompt=1, guidance_scale=4.0)
    images = decoder(image=zero_img, strength=1.0, image_embeds=img_emb, negative_image_embeds=negative_emb.negative_image_embeds, num_inference_steps=250, height=704, width=1280, guidance_scale=4.0).images
    if face_image is not None:
        images[0] = delete_bg(face_image, images[0])
    if text is not None:
        img = deepcopy(images[0])
        W, H = img.size
        print(len(text))
        if len(text) < 52:
            myFont = ImageFont.truetype('cene655/drawbench/DejaVuSansCondensed.ttf', 50)
        else:
            myFont = ImageFont.truetype('cene655/drawbench/DejaVuSansCondensed.ttf', 35)
        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), text, font=myFont)
        draw.text(((W-w)/2, 25), text, font=myFont, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        #images2 = controlnet(image=img, strength=0.01, image_embeds=img_emb, negative_image_embeds=negative_emb.image_embeds, hint=hint, num_inference_steps=150, height=img.size[1], width=img.size[0])
        return img#images2[0][0]
    else:
        return images[0]

def generate_banner(decoder, prior, prompt, text=None, style_image=None, face_image=None, animation=None):
    prompt = prepare_caption(prompt)
    prompt = '4k photo of ' + prompt
    zero_img = PIL.Image.new(mode="RGB", size=(200, 200))
    img_emb = prior(prompt=prompt, num_inference_steps=50, num_images_per_prompt=1, guidance_scale=1.5).image_embeds
    if style_image is not None:
        img_emb2 = prior.interpolate(images_and_prompts=[style_image], weights=[1.0], num_inference_steps=25, num_images_per_prompt=1, guidance_scale=4.0).image_embeds
        img_emb = img_emb * 0.75 + img_emb2 * 0.25
    negative_emb = prior(prompt='blow quility', num_inference_steps=25, num_images_per_prompt=1, guidance_scale=4.0)
    images = decoder(image=zero_img, strength=1.0, image_embeds=img_emb, negative_image_embeds=negative_emb.negative_image_embeds, num_inference_steps=100, height=896, width=2240, guidance_scale=4.0).images
    if face_image is not None:
        images[0] = delete_bg(face_image, images[0])
    if text is not None:
        img = deepcopy(images[0])
        W, H = img.size
        if len(text) < 52:
            myFont = ImageFont.truetype('DejaVuSansCondensed.ttf', 100)
        else:
            myFont = ImageFont.truetype('DejaVuSansCondensed.ttf', 35)
        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), text, font=myFont)
        draw.text(((W-w)/2, (H-h)/2), text, font=myFont, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        return img.resize((2204, 864))
    else:
        return images[0].resize((2204, 864))
