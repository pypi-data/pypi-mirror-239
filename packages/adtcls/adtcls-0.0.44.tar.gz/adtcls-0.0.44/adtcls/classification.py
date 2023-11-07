import os
import json
import yaml
import time
import cv2
from PIL import Image
import numpy as np
import logging
try:
    from service.exchange.SyncObj import globalSharingService as g
except:
    pass
from .config import model_registry
from .src import BaseTrain
from .src import Evaluate,get_classes
from .src import train_pipeline_main,load_cls_model

class FileUtils:
    def load_yaml(self, config_file):
        with open(config_file, "r") as f:
            config_txt = f.read()
            config = yaml.load(config_txt, Loader=yaml.FullLoader)
        return config
    
    def load_json(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            file = json.load(f)
        return file
    
    def load_txt(self, txt_file):
        content = open(txt_file, 'r').readlines()
        content = [item.strip('\n') for item in content]
        return content
    
class Classification(FileUtils):
    def __init__(self,modelId=None):
        self.task_type = 0
        if not modelId is None:
            saved_model_list = os.listdir('modelfile')
            saved_model_list = [item for item in saved_model_list if '-' in item and 'pth' in item and \
                                                                     (item.split('-')[0]==modelId or \
                                                                     eval(item.split('-')[0])==modelId)]
            if len(saved_model_list):
                try:
                    model_name   = saved_model_list[0]
                    model_path   = f'modelfile/{model_name}'
                    backbone     = model_name.split('-')[1]
                    input_shape  = eval(model_name.split('-')[2])
                    classes_path = f'modelfile/{modelId}-classes.txt'
                    cuda         = False
                    self.model   = load_cls_model(model_path=model_path,backbone=backbone,input_shape=input_shape,
                                                  classes_path=classes_path,cuda=cuda)
                    self.classes,self.num_class = get_classes(classes_path)
                    self.model_path = model_path
                except Exception as e:
                    print('model loading error', e)                
    
    def train(self,base_path,model_name='resnet50', model_id=0, cuda=True, **kwargs):
        '''
        Args:
            base_path: under which checkpoint and log will be created
            model_name: select a classification model
            model_id: used to created dataset folder, log folder and model name 
        '''
        param_registor = model_registry[model_name]
        param = param_registor()
        args = BaseTrain(param).parse_args()
        
        args.cuda = cuda
        args.class_file = os.path.join(base_path,'dataset',f'{model_id}','classes.txt')
        args.train_file = os.path.join(base_path,'dataset',f'{model_id}','train.txt')
        args.val_file   = os.path.join(base_path,'dataset',f'{model_id}','val.txt')
        args.save_dir   = base_path
        args.unfreeze_epoch = 1
        args.model_name = model_id
        for k,v in kwargs.items():
            if hasattr(args, k):
                try:
                    setattr(args, k, v)
                except:
                    continue
        train_pipeline_main(args)
        
        model_path = os.path.join(base_path,'checkpoint',f'{model_id}','best_epoch_weights.pth')
        self.evaluator = Evaluate(model_path=model_path,
                                  val_file=args.val_file,
                                  class_file=args.class_file,
                                  backbone=args.back_bone,
                                  cuda=args.cuda)
        TPositives,FPositives = self.evaluate()
        res_bar = [FPositives,TPositives]
        
        res,res_line = {},{}
        eval_period = 1
        epoch_val_loss = self.load_txt(os.path.join(base_path, f'log/loss_{model_id}', 'epoch_val_loss.txt'))
        epoch_acc      = self.load_txt(os.path.join(base_path, f'log/loss_{model_id}', 'epoch_acc.txt'))
        epoch_len      = min(len(epoch_val_loss), len(epoch_acc))
        res_line['Train Lose']     = [[(ep+1)*eval_period, round(eval(epoch_val_loss[ep]), 2)] for ep in range(epoch_len)]
        res_line['Train Accuracy'] = [[(ep+1)*eval_period, eval(epoch_acc[ep])] for ep in range(epoch_len)]
        res_line = json.dumps(res_line)
        
        for i,bar in enumerate(res_bar):
            res_bar[i] = {eval(key):val for key,val in res_bar[i].items()}
            res_bar[i] = sorted(res_bar[i].items(), key=lambda x: x[0])
            res_bar[i] = {item[0]:item[1] for item in res_bar[i]}
            res_bar[i] = json.dumps(res_bar[i])

        res['barChart']   = res_bar[0]
        res['barChart1']  = res_bar[1]
        res['lineChart']  = res_line
        res['modelId']    = model_id
        res['id']         = 0
        res['isDeleted']  = 0
        res['createTime'] = 0
        res = str(json.dumps(res))
        self.delete_id(base_path, model_name, args.input_size, model_id)
        
        return res
    
    def evaluate(self,):
        return self.evaluator.main()
    
    def inference(self, **kwargs):
        try:
            img_list = sorted(kwargs.items(), key=lambda x: x[0])
            img_list = [item[1] for item in img_list]
            image = Image.fromarray(cv2.cvtColor(cv2.hconcat(img_list),cv2.COLOR_BGR2RGB))
            pred_lbl,pred_conf = self.model.detect_image_cls(image)
            return int(self.classes[int(pred_lbl)]),pred_conf
        except Exception as e:
            logging.warning(e)
        return None
    
    def delete_id(self, base_path, model_name, input_shape, model_id):
        '''
        notes: delete related dataset, log, checkpoint after evaluation
        '''
        import shutil        
        os.makedirs('modelfile', exist_ok=True)
        shutil.copyfile(os.path.join(base_path, f'dataset/{model_id}', 'classes.txt'), 
                        f'modelfile/{model_id}-classes.txt')
        shutil.copyfile(os.path.join(base_path, f'checkpoint/{model_id}/best_epoch_weights.pth'), 
                        f'modelfile/{model_id}-{model_name}-{input_shape}-.pth')
        shutil.rmtree(os.path.join(base_path, f'dataset/{model_id}'))
        shutil.rmtree(os.path.join(base_path, f'log/loss_{model_id}'))
        shutil.rmtree(os.path.join(base_path, f'checkpoint/{model_id}'))
    