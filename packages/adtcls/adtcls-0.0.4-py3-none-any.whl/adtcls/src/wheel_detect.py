import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from glob import glob
import cv2
import numpy as np
from PIL import Image
from src.yolo import YOLO
from tqdm import tqdm

if __name__ == "__main__":
    cuda = True
    model = YOLO(model_path='./checkpoint/wheel_detection_weights.pth',\
                 phi = 'nano',
                 cuda=cuda,
                 classes_path='wheel_classes.txt')
    input_path = input('input image folder for inference:')
    img_folder = glob(os.path.join(input_path, '*.jpg'))+glob(os.path.join(input_path, '*.png'))
    for img_path in tqdm(img_folder):
        img_path = img_path.replace('\\', '/')
        img_name = img_path.split('/')[-1]
        model.cut_image(Image.open(img_path),crop=True,img_name=img_name)