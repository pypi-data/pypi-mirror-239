import logging
import argparse
from src import ConfigUtils

class BaseTrain():
    def __init__(self,base_config='config/base.yaml', model_config='config/resnet50.yaml'):
        logging.basicConfig(level=logging.INFO)
#         logging.getLogger("BaseTrain")
#         self.log = logging.getLogger("BaseTrain").setLevel(logging.INFO) 
        self.parser = argparse.ArgumentParser(description='run pipeline training')
        self.base_config, self.base_config_txt = ConfigUtils.load_yaml_config(base_config)
        self.model_config, self.model_config_txt = ConfigUtils.load_yaml_config(model_config)

    def parse_args(self):
        #------------------------
        #  base config: model
        #------------------------
        self.parser.add_argument("--model", type=str, default=self.base_config['model']['default'], help="pretrained model weights")
        self.parser.add_argument("--optimizer", type=str, default=self.base_config['model']['optimizer'], help="train optimizer")
        #------------------------
        #  base config: train
        #------------------------
        self.parser.add_argument('--cuda', type=bool, default=self.base_config['train']['cuda'], help="using gpu training")
        self.parser.add_argument('--distributed', type=bool, default=self.base_config['train']['distributed'], help="distributed training")
        self.parser.add_argument('--fp16', type=bool, default=self.base_config['train']['distributed'], help="fp16 weights")
        self.parser.add_argument('--num_worker', type=bool, default=self.base_config['train']['num_worker'], help="nums of worker")
        self.parser.add_argument('--class_file', type=str, default=self.base_config['train']['class_file'], help="containing class info")
        self.parser.add_argument('--train_file', type=str, default=self.base_config['train']['train_file'], help="train dataset")
        self.parser.add_argument('--val_file', type=str, default=self.base_config['train']['val_file'], help="val dataset")
        self.parser.add_argument('--freeze_train', type=bool, default=self.base_config['train']['freeze_train'], help="dont change")
        self.parser.add_argument('--init_epoch', type=int, default=self.base_config['train']['init_epoch'], help="dont change")
        self.parser.add_argument('--freeze_epoch', type=int, default=self.base_config['train']['freeze_epoch'], help="freeze train epoch")
        self.parser.add_argument('--freeze_batch_size', type=int, default=self.base_config['train']['freeze_batch_size'], \
                            help="batch size during freeze train")
        self.parser.add_argument('--unfreeze_epoch', type=int, default=self.base_config['train']['unfreeze_epoch'],help="end epoch")
        self.parser.add_argument('--unfreeze_batch_size', type=int, default=self.base_config['train']['freeze_batch_size'], \
                            help="batch size during unfreeze train")
        self.parser.add_argument('--save_period', type=int, default=self.base_config['train']['save_period'],\
                                 help="save a chkpt every certain period")   
        self.parser.add_argument('--momentum', type=float, default=self.base_config['train']['momentum'], help="optimizer momentum")
        self.parser.add_argument('--lr_decay_type', type=str, default=self.base_config['train']['lr_decay_type'], help="[cos, step]")
        self.parser.add_argument('--init_lr', type=float, default=self.base_config['train'][self.base_config['model']['optimizer']]['init_lr'],\
                            help="init learning rate")
        self.parser.add_argument('--min_lr', type=float, default=self.base_config['train'][self.base_config['model']['optimizer']]['min_lr'],\
                            help="init learning rate")
        self.parser.add_argument('--weight_decay', type=float, default=self.base_config['train'][self.base_config['model']['optimizer']]['weight_decay'], help="init learning rate")
        #------------------------
        #  base config: evaluate
        #------------------------
        self.parser.add_argument('--num_class', type=int, default=self.base_config['evaluate']['num_class'], help="num of class")
        self.parser.add_argument('--max_box', type=int, default=self.base_config['evaluate']['max_box'], help="max boxes on single image")
        self.parser.add_argument('--confidence', type=float, default=self.base_config['evaluate']['confidence'], nargs='?', help="confidence threshold")
        self.parser.add_argument('--nms_iou', type=float, default=self.base_config['evaluate']['nms_iou'], help="nms ious threshold")
        self.parser.add_argument('--conf_variable', type=dict, default=self.base_config['confvariable']['variables'], help="conf variables")

        #-----------------------------
        #  base config: augmentation
        #-----------------------------
        self.parser.add_argument('--aug_ratio', type=float, default=self.base_config['augmentation']['aug_ratio'], help="aug applied epochs")
        self.parser.add_argument('--mosaic', type=bool, default=self.base_config['augmentation']['mosaic'], help="mosaic augmentation")
        self.parser.add_argument('--mosaic_prob', type=float, default=self.base_config['augmentation']['mosaic_prob'], help="mosaic applied prob")
        self.parser.add_argument('--mixup', type=bool, default=self.base_config['augmentation']['mixup'], help="mixup augmentation")
        self.parser.add_argument('--mixup_prob', type=float, default=self.base_config['augmentation']['mixup_prob'], help="mixup_prob")
        #-----------------------------
        #  model config: model info
        #-----------------------------
        self.parser.add_argument('--back_bone', type=str, default=self.model_config['model']['back_bone'], help="choosing pretrained backbone")
        self.parser.add_argument('--input_size', type=list, default=self.model_config['model']['input_size'], help="image size")
        self.parser.add_argument('--model_path', type=str, default=self.model_config['model']['model_path'], help="weight path")
        self.parser.add_argument('--phi', type=str, default=self.model_config['model']['phi'], help="model size")
        self.parser.add_argument('--model_name', type=str, default='', help="name for checkpoint, log")
        self.args = self.parser.parse_args()
        return self.args
    
#     def required_args(desc='run pipeline training'):
#         parser = argparse.ArgumentParser(description=desc)
#         parser.add_argument("--base_config", type=str, default='config/detection/base.yaml', help="base yaml file", required=False)
#         parser.add_argument("--model_config", type=str, default='config/detection/yolox_tiny.yaml', help="model yaml file", required=False)
#         args = parser.parse_args()
#         return args
    
