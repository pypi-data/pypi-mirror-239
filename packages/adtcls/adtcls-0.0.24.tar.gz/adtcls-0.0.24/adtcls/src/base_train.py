import logging
import argparse
from . import ConfigUtils

class BaseTrain():
    def __init__(self,param):
        logging.basicConfig(level=logging.INFO)
        self.parser = argparse.ArgumentParser(description='run pipeline training')
        self.param  = param

    def parse_args(self):
        #------------------------
        #  base config: model
        #------------------------
        self.parser.add_argument("--model", type=str, default=self.param.model.default, help="pretrained model weights")
        self.parser.add_argument("--optimizer", type=str, default=self.param.model.optimizer, help="train optimizer")
        #------------------------
        #  base config: train
        #------------------------
        self.parser.add_argument('--cuda', type=bool, default=self.param.train.cuda, help="using gpu training")
        self.parser.add_argument('--distributed', type=bool, default=self.param.train.distributed, help="distributed training")
        self.parser.add_argument('--fp16', type=bool, default=self.param.train.distributed, help="fp16 weights")
        self.parser.add_argument('--num_worker', type=bool, default=self.param.train.num_worker, help="nums of worker")
        self.parser.add_argument('--class_file', type=str, default=self.param.train.class_file, help="containing class info")
        self.parser.add_argument('--train_file', type=str, default=self.param.train.train_file, help="train dataset")
        self.parser.add_argument('--val_file', type=str, default=self.param.train.val_file, help="val dataset")
        self.parser.add_argument('--freeze_train', type=bool, default=self.param.train.freeze_train, help="dont change")
        self.parser.add_argument('--init_epoch', type=int, default=self.param.train.init_epoch, help="dont change")
        self.parser.add_argument('--freeze_epoch', type=int, default=self.param.train.freeze_epoch, help="freeze train epoch")
        self.parser.add_argument('--freeze_batch_size', type=int, default=self.param.train.freeze_batch_size, \
                            help="batch size during freeze train")
        self.parser.add_argument('--unfreeze_epoch', type=int, default=self.param.train.unfreeze_epoch,help="end epoch")
        self.parser.add_argument('--unfreeze_batch_size', type=int, default=self.param.train.freeze_batch_size, \
                            help="batch size during unfreeze train")
        self.parser.add_argument('--save_period', type=int, default=self.param.train.save_period,\
                                 help="save a chkpt every certain period")   
        self.parser.add_argument('--momentum', type=float, default=self.param.train.momentum, help="optimizer momentum")
        self.parser.add_argument('--lr_decay_type', type=str, default=self.param.train.lr_decay_type, help=".cos, step.")
        self.parser.add_argument('--init_lr', type=float, default=getattr(self.param.train,self.param.model.optimizer).init_lr,\
                            help="init learning rate")
        self.parser.add_argument('--min_lr', type=float, default=getattr(self.param.train,self.param.model.optimizer).min_lr,\
                            help="init learning rate")
        self.parser.add_argument('--weight_decay', type=float, default=getattr(self.param.train,self.param.model.optimizer).weight_decay, help="init learning rate")
        #------------------------
        #  base config: evaluate
        #------------------------
        self.parser.add_argument('--num_class', type=int, default=self.param.evaluate.num_class, help="num of class")
        self.parser.add_argument('--max_box', type=int, default=self.param.evaluate.max_box, help="max boxes on single image")
        self.parser.add_argument('--confidence', type=float, default=self.param.evaluate.confidence, nargs='?', help="confidence threshold")
        self.parser.add_argument('--nms_iou', type=float, default=self.param.evaluate.nms_iou, help="nms ious threshold")
        self.parser.add_argument('--conf_variable', type=dict, default=self.param.confvariable.variables, help="conf variables")

        #-----------------------------
        #  base config: augmentation
        #-----------------------------
        self.parser.add_argument('--aug_ratio', type=float, default=self.param.augmentation.aug_ratio, help="aug applied epochs")
        self.parser.add_argument('--mosaic', type=bool, default=self.param.augmentation.mosaic, help="mosaic augmentation")
        self.parser.add_argument('--mosaic_prob', type=float, default=self.param.augmentation.mosaic_prob, help="mosaic applied prob")
        self.parser.add_argument('--mixup', type=bool, default=self.param.augmentation.mixup, help="mixup augmentation")
        self.parser.add_argument('--mixup_prob', type=float, default=self.param.augmentation.mixup_prob, help="mixup_prob")
        #-----------------------------
        #  model config: model info
        #-----------------------------
        self.parser.add_argument('--back_bone', type=str, default=self.param.model.back_bone, help="choosing pretrained backbone")
        self.parser.add_argument('--input_size', type=list, default=self.param.model.input_size, help="image size")
        self.parser.add_argument('--model_path', type=str, default=self.param.model.model_path, help="weight path")
        self.parser.add_argument('--phi', type=str, default=self.param.model.phi, help="model size")
        self.parser.add_argument('--model_name', type=str, default='', help="name for checkpoint, log")
        self.parser.add_argument('--save_dir', type=str, default='', help="base save dir")
#         self.args = self.parser.parse_args()
        self.args,_ = self.parser.parse_known_args()
        return self.args

    
