# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:19:35 2021

@author: emilk
"""

from glob import glob
import numpy as np
import cv2
from PIL import Image
from torchvision import transforms
import torch
from nets.MobileNetV2_unet import MobileNetV2_unet
import matplotlib.pyplot as plt


# load pre-trained model and weights
def load_model():
    model = MobileNetV2_unet(None).to(torch.device("cpu"))
    state_dict = torch.load('model.pt', map_location='cpu')
    model.load_state_dict(state_dict)
    model.eval()
    return model

#założenie że obraz 1:1
def Predict_Img(img_path,zapis_path):
    
    model = load_model()
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    print('Model loaded')
    
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pil_img = Image.fromarray(image)
    torch_img = transform(pil_img)
    torch_img = torch_img.unsqueeze(0)
    torch_img = torch_img.to(torch.device("cpu"))
    
    
    # Forward Pass
    logits = model(torch_img)
    mask = np.argmax(logits.data.cpu().numpy(), axis=1)
   
    plt.figure(frameon=False)
    plt.axis('off')
    plt.imshow(mask.squeeze(), interpolation='nearest')
    plt.savefig(zapis_path+"/wynik.png", bbox_inches='tight', dpi=199, pad_inches=0)
    plt.show()
    