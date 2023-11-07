import sys
import os
import numpy as np
from PIL import Image
import torch
from .classification import (Classification, cvtColor, letterbox_image, preprocess_input)
from . import get_classes

# def get_classes(classes_path):
#     with open(classes_path, encoding='utf-8') as f:
#         class_names = f.readlines(1)
#     class_names = eval(class_names[0])
#     class_names = [item for item in class_names]
#     class_names = [c.strip() for c in class_names]
#     return class_names, len(class_names)

class Evaluate():
    def __init__(self,model_path,val_file,class_file,backbone,cuda):
        self.val_file = val_file
        self.detector = Classification(
                        model_path = model_path,\
                        classes_path = class_file,\
                        backbone = backbone,
                        cuda = cuda
                        )
        self.class_names,self.num_class = get_classes(class_file)
        
    def main(self):
        val_lines = open(self.val_file, 'r').readlines()
        val_gt = [eval(item.split(';')[0]) for item in val_lines]
        val_img = [item.split(';')[1].strip('\n') for item in val_lines]
        FPositives = {cls:0 for cls in self.class_names}
        TPositives = {cls:0 for cls in self.class_names}
        for i,img_path in enumerate(val_img):
            image = Image.open(img_path)
            result,_ = self.detector.detect_image_cls(image)
            if not result==val_gt[i]:
                if result>self.num_class:
                    print(f'pred result {result} not in ground truth...')
                else:
                    FPositives[self.class_names[int(result)]] += 1
            elif result==val_gt[i]:
                if result>self.num_class:
                    print(f'pred result {result} not in ground truth...')
                else:
                    TPositives[self.class_names[int(result)]] += 1
        return TPositives,FPositives
