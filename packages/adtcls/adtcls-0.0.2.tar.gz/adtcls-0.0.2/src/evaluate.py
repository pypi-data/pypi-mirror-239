import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from PIL import Image
import torch

from src.classification import (Classification, cvtColor, letterbox_image, preprocess_input)
# from src.utils.utils import letterbox_image

test_model_path    = 'checkpoint/2023_11_01_13_21_59/best_epoch_weights.pth'
test_val_path   = 'dataset/glass/cls_val.txt'
test_classes_path   = 'dataset/glass/cls_classes.txt'
test_cuda        = True

def get_classes(classes_path):
    with open(classes_path, encoding='utf-8') as f:
        class_names = f.readlines(1)
#     class_names = [c.strip() for c in class_names]
    class_names = eval(class_names[0])
    class_names = [item for item in class_names]
    class_names = [c.strip() for c in class_names]
    return class_names, len(class_names)

class Evaluate():
    def __init__(self,model_path,val_file,class_file,cuda):
        self.val_file = val_file
        self.detector = Classification(
                        model_path = model_path,\
                        classes_path = class_file,\
                        cuda = cuda
                        )
        self.class_names,_ = get_classes(class_file)
        
    def main(self):
        val_lines = open(self.val_file, 'r').readlines()
        val_gt = [eval(item.split(';')[0]) for item in val_lines]
        val_img = [item.split(';')[1].strip('\n') for item in val_lines]
        classes = set(val_gt)
        results = {self.class_names[int(cls)]:0 for cls in classes}
        for i,img_path in enumerate(val_img):
            image = Image.open(img_path)
            result = self.detector.detect_image_cls(image)
            if not result==val_gt[i]:
                if not result in classes:
                    print(f'pred result {result} not in ground truth...')
                else:
                    print(f'image path: {img_path}, gt: {self.class_names[val_gt[i]]}, pred: {self.class_names[int(result)]}')
                    results[self.class_names[int(result)]] += 1
        return results
    
if __name__ == "__main__":
    evaluate = Evaluate(test_model_path,test_val_path,test_classes_path,test_cuda)
    results = evaluate.main()
    print(results)
