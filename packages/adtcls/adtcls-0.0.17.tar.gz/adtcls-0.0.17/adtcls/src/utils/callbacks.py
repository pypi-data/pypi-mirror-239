import datetime
import sys
import os
import torch
import torch.nn.functional as F
# from ignite.metrics.recall import Recall
# from ignite.metrics.precision import Precision
import matplotlib
matplotlib.use('Agg')
import scipy.signal
from matplotlib import pyplot as plt
#from torch.utils.tensorboard import SummaryWriter
from PIL import Image
from tqdm import tqdm
import numpy as np
from .utils import resize_image,cvtColor,preprocess_input

class LossHistory():
    def __init__(self, log_dir, model, input_shape):
#         time_str        = datetime.datetime.strftime(datetime.datetime.now(),'%Y_%m_%d_%H_%M_%S')
        self.log_dir    = log_dir
        self.losses     = []
        self.val_loss   = []
        self.val_acc    = []
        
        os.makedirs(self.log_dir, exist_ok=True)
#         self.writer     = SummaryWriter(self.log_dir)
#         try:
#             dummy_input     = torch.randn(2, 3, input_shape[0], input_shape[1])
#             self.writer.add_graph(model, dummy_input)
#         except:
#             pass

    def append_loss(self, epoch, loss, val_loss):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        self.losses.append(loss)
        self.val_loss.append(val_loss)

        with open(os.path.join(self.log_dir, "epoch_loss.txt"), 'a') as f:
            f.write(str(loss))
            f.write("\n")
        with open(os.path.join(self.log_dir, "epoch_val_loss.txt"), 'a') as f:
            f.write(str(val_loss))
            f.write("\n")

#         self.writer.add_scalar('loss', loss, epoch)
#         self.writer.add_scalar('val_loss', val_loss, epoch)
        self.loss_plot()
    
    def append_acc(self, val_acc):
        self.val_acc.append(val_acc)
        
    def loss_plot(self):
        iters = range(len(self.losses))

        plt.figure()
        plt.plot(iters, self.losses, 'red', linewidth = 2, label='train loss')
        plt.plot(iters, self.val_loss, 'coral', linewidth = 2, label='val loss')
        try:
            if len(self.losses) < 25:
                num = 5
            else:
                num = 15
            
            plt.plot(iters, scipy.signal.savgol_filter(self.losses, num, 3), 'green', linestyle = '--', linewidth = 2, label='smooth train loss')
            plt.plot(iters, scipy.signal.savgol_filter(self.val_loss, num, 3), '#8B4513', linestyle = '--', linewidth = 2, label='smooth val loss')
        except:
            pass

        plt.grid(True)
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend(loc="upper right")

        plt.savefig(os.path.join(self.log_dir, "epoch_loss.png"))

        plt.cla()
        plt.close("all")

class EvalCallback():
    def __init__(self, net, input_shape, class_names, num_classes, val_lines, log_dir, cuda,\
                 letterbox_image=True, MINOVERLAP=0.5, eval_flag=True, period=1):
        super(EvalCallback, self).__init__()
        
        self.net                = net
        self.input_shape        = input_shape
        self.class_names        = class_names
        self.num_classes        = num_classes
        self.val_lines          = val_lines
        self.log_dir            = log_dir
        self.cuda               = cuda
        self.letterbox_image    = letterbox_image
        self.MINOVERLAP         = MINOVERLAP
        self.eval_flag          = eval_flag
        self.period             = period
        
        self.maps       = [0]
        self.epoches    = [0]

    def get_map_txt(self, image, class_names):
        image_shape = np.array(np.shape(image)[0:2])
        image       = cvtColor(image)
        image_data  = resize_image(image, (self.input_shape[1],self.input_shape[0]), self.letterbox_image)
        image_data  = np.expand_dims(np.transpose(preprocess_input(np.array(image_data, dtype='float32')), (2, 0, 1)), 0)

        with torch.no_grad():
            images = torch.from_numpy(image_data)
            if self.cuda:
                images = images.cuda()
            results = self.net(images)
        results = torch.argmax(F.softmax(results, dim=-1), dim=-1).squeeze()              
        return results
    
    def on_epoch_end(self, epoch, model_eval):
        if epoch % self.period == 0 and self.eval_flag:
            f = open(os.path.join(self.log_dir, 'epoch_acc'+".txt"),"a") 
            self.net = model_eval
            os.makedirs(self.log_dir, exist_ok=True)
            print("Get map.")
            confusion_map = [[0]*(self.num_classes+1)]
            confusion_map[0] = [0]+self.class_names
            for i in range(1,self.num_classes+1):
                confusion_map.append([self.class_names[i-1]]+[0]*self.num_classes)
            tp,total = 0,0
            for annotation_line in tqdm(self.val_lines):
                line        = annotation_line.split(';')
                image       = Image.open(line[1])
                gt         = eval(line[0])
#                 if self.cuda:
#                     gt = torch.as_tensor(gt, dtype=torch.float32).cuda()
#                 else:
#                     gt = torch.as_tensor(gt, dtype=torch.float32)
                #------------------------------#
                #   获得预测txt
                #------------------------------#
                results = self.get_map_txt(image, self.class_names).type(torch.int32).detach().cpu().numpy()
                confusion_map[gt+1][results+1] += 1
                tp += (results==gt)
                total += 1
#                 if not results==gt:
#                     print(line[1], f'gt:{self.class_names[gt]}', f'pred:{self.class_names[results]}')
#             for i in range(1, self.num_classes+1):
#                 if i==1:
#                     print(f'{"":15}',f'{confusion_map[0][i]:10}',end='')
#                 else:
#                     print(f'{confusion_map[0][i]:10}',end='')
#             print('\r')
#             for i in range(self.num_classes):
#                 for j in range(self.num_classes+1):
#                     print(f'{confusion_map[i+1][j]:10}',end='')
#                 print('\r')

            acc = '{:.2f}'.format(tp/max(1,total))
            f.write(acc)
            f.write('\n')
            f.close()