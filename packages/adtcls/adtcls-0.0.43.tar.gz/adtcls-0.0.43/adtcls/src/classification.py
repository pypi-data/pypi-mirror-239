import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torchvision.models import (resnet18,resnet34,resnet50,resnet101,resnet152,inception_v3,mobilenet_v2,mobilenet_v3_large,shufflenet_v2_x1_5)
from torchvision.models._utils import IntermediateLayerGetter

# from net import get_model_from_name
from .utils.utils import (cvtColor, get_classes, letterbox_image,
                         preprocess_input, show_config)


#--------------------------------------------#
#   使用自己训练好的模型预测需要修改3个参数
#   model_path和classes_path和backbone都需要修改！
#--------------------------------------------#
class Classification(object):
    _defaults = {
        #--------------------------------------------------------------------------#
        #   使用自己训练好的模型进行预测一定要修改model_path和classes_path！
        #   model_path指向logs文件夹下的权值文件，classes_path指向model_data下的txt
        #   如果出现shape不匹配，同时要注意训练时的model_path和classes_path参数的修改
        #--------------------------------------------------------------------------#
        "model_path"        : 'log/best_epoch_weights.pth',
        "classes_path"      : 'cls_classes.txt',
        #--------------------------------------------------------------------#
        #   输入的图片大小
        #--------------------------------------------------------------------#
        "input_shape"       : [256, 256],
        #--------------------------------------------------------------------#
        #   所用模型种类：
        #   mobilenetv2、
        #   resnet18、resnet34、resnet50、resnet101、resnet152
        #   vgg11、vgg13、vgg16、vgg11_bn、vgg13_bn、vgg16_bn、
        #   vit_b_16、
        #   swin_transformer_tiny、swin_transformer_small、swin_transformer_base
        #--------------------------------------------------------------------#
        "backbone"          : 'mobilenetv3',
        "backbone_map"       : {'resnet18':resnet18, 'resnet34':resnet34, 'resnet50':resnet50, 'resnet101':resnet101, 'resnet152':resnet152,'inception_v3':inception_v3, 'mobilenetv2':mobilenet_v2, 'mobilenetv3':mobilenet_v3_large, 'shufflenetv2':shufflenet_v2_x1_5},
        #--------------------------------------------------------------------#
        #   该变量用于控制是否使用letterbox_image对输入图像进行不失真的resize
        #   否则对图像进行CenterCrop
        #--------------------------------------------------------------------#
        "letterbox_image"   : False,
        #-------------------------------#
        #   是否使用Cuda
        #   没有GPU可以设置成False
        #-------------------------------#
        "cuda"              : True
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    #---------------------------------------------------#
    #   初始化classification
    #---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)

        #---------------------------------------------------#
        #   获得种类
        #---------------------------------------------------#
        self.class_names, self.num_classes = get_classes(self.classes_path)
        self.generate()
        
#         show_config(**self._defaults)

    #---------------------------------------------------#
    #   获得所有的分类
    #---------------------------------------------------#
    def generate(self):
        #---------------------------------------------------#
        #   载入模型与权值
        #---------------------------------------------------#
        self.model = self.backbone_map[self.backbone](pretrained=False)
        if 'resnet' in self.backbone or 'inception' in self.backbone:
            fc_inputs = self.model.fc.in_features
            self.model.fc = nn.Linear(fc_inputs, self.num_classes)
        elif 'vit' in self.backbone:
            head_inputs = self.model.heads.head.in_features
            self.model.heads.head = nn.Linear(head_inputs, self.num_classes)
        elif 'swin' in self.backbone:
            head_inputs = self.model.head.in_features
            self.model.head = nn.Linear(head_inputs, self.num_classes)
        elif 'mobile' in self.backbone:
            fc_inputs = self.model.classifier[-1].in_features
            self.model.classifier[-1] = nn.Linear(fc_inputs, self.num_classes)
    #         model.classifier = nn.Sequential(nn.Dropout(0.2),nn.Linear(in_features=1280,out_features=num_classes,bias=True))
        elif 'shuffle' in self.backbone:
            fc_inputs = self.model.fc.in_features
            self.model.fc = nn.Linear(fc_inputs, self.num_classes)
            
#         if self.backbone not in ['vit_b_16', 'swin_transformer_tiny', 'swin_transformer_small', 'swin_transformer_base']:
#             self.model  = get_model_from_name[self.backbone](num_classes = self.num_classes, pretrained = False)
#         else:
#             self.model  = get_model_from_name[self.backbone](input_shape = self.input_shape, num_classes = self.num_classes, pretrained = False)
        device      = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.load_state_dict(torch.load(self.model_path, map_location=device))
        self.model  = self.model.eval()
        print('{} model, and classes loaded.'.format(self.model_path))

        if self.cuda:
            self.model = nn.DataParallel(self.model)
            self.model = self.model.cuda()

    #---------------------------------------------------#
    #   检测图片
    #---------------------------------------------------#
    def detect_image(self, image):
        #---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        #   代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
        #---------------------------------------------------------#
        image       = cvtColor(image)
        #---------------------------------------------------#
        #   对图片进行不失真的resize
        #---------------------------------------------------#
        image_data  = letterbox_image(image, [self.input_shape[1], self.input_shape[0]], self.letterbox_image)
        #---------------------------------------------------------#
        #   归一化+添加上batch_size维度+转置
        #---------------------------------------------------------#
        image_data  = np.transpose(np.expand_dims(preprocess_input(np.array(image_data, np.float32)), 0), (0, 3, 1, 2))

        with torch.no_grad():
            photo   = torch.from_numpy(image_data)
            if self.cuda:
                photo = photo.cuda()
            #---------------------------------------------------#
            #   图片传入网络进行预测
            #---------------------------------------------------#
            preds   = torch.softmax(self.model(photo)[0], dim=-1).cpu().numpy()
        #---------------------------------------------------#
        #   获得所属种类
        #---------------------------------------------------#
        class_name  = self.class_names[np.argmax(preds)]
        probability = np.max(preds)

        #---------------------------------------------------#
        #   绘图并写字
        #---------------------------------------------------#
        plt.subplot(1, 1, 1)
        plt.imshow(np.array(image))
        plt.title('Class:%s Probability:%.3f' %(class_name, probability))
        plt.show()
        return class_name
    
    def detect_image_cls(self, image):
        image       = cvtColor(image)
        image_data  = letterbox_image(image, [self.input_shape[1], self.input_shape[0]], self.letterbox_image)
        image_data  = np.transpose(np.expand_dims(preprocess_input(np.array(image_data, np.float32)), 0), (0, 3, 1, 2))
        
        with torch.no_grad():
            photo   = torch.from_numpy(image_data).type(torch.FloatTensor)
            if self.cuda:
                photo = photo.cuda()
            preds   = torch.softmax(self.model(photo)[0], dim=-1).cpu().numpy()
        pred   = np.argmax(preds)
        return pred, np.max(preds)
    
    def get_image_feature(self, image):
        image       = cvtColor(image)
        image_data  = letterbox_image(image, [self.input_shape[1], self.input_shape[0]], self.letterbox_image)
        image_data  = np.transpose(np.expand_dims(preprocess_input(np.array(image_data, np.float32)), 0), (0, 3, 1, 2))
        
        feature_out = IntermediateLayerGetter(self.model, {'avgpool':'feature'})
        feature = feature_out(torch.from_numpy(image_data))['feature'].flatten()
        return feature
#         with torch.no_grad():
#             photo   = torch.from_numpy(image_data)
#             if self.cuda:
#                 photo = photo.cuda()
#             #---------------------------------------------------#
#             #   图片传入网络进行预测
#             #---------------------------------------------------#
#             preds   = torch.softmax(self.model(photo)[0], dim=-1).cpu().numpy()
#         #---------------------------------------------------#
#         #   获得所属种类
#         #---------------------------------------------------#
#         class_name  = self.class_names[np.argmax(preds)]
#         probability = np.max(preds)

#         #---------------------------------------------------#
#         #   绘图并写字
#         #---------------------------------------------------#
#         plt.subplot(1, 1, 1)
#         plt.imshow(np.array(image))
#         plt.title('Class:%s Probability:%.3f' %(class_name, probability))
#         plt.show()
#         return class_name
    
