import os

from .config import model_registry
from .src import BaseTrain
from .src import Evaluate
from .src.train import main

class Classification():
    def __init__(self,):
        pass
    
    def train(self,base_path,model_name='resnet50', model_id=0, cuda=True):
        '''
        Args:
            base_path: under which checkpoint and log will be created
            model_name: select a classification model
            model_id: used to created dataset folder, log folder and model name 
        '''
        param_registor = model_registry[model_name]
        param = param_registor()
        self.args = BaseTrain(param).parse_args()
        
        self.args.cuda = cuda
        self.args.class_file = os.path.join(base_path,'dataset',f'{model_id}','classes.txt')
        self.args.train_file = os.path.join(base_path,'dataset',f'{model_id}','train.txt')
        self.args.val_file   = os.path.join(base_path,'dataset',f'{model_id}','val.txt')
        self.args.save_dir   = base_path
        self.args.unfreeze_epoch = 1
        self.args.model_name = model_id
        main(self.args)
        
        model_path = os.path.join(base_path,'checkpoint',f'{model_id}','best_epoch_weights.pth')
        self.evaluator = Evaluate(model_path=model_path,
                                  val_file=self.args.val_file,
                                  class_file=self.args.class_file,
                                  backbone=self.args.back_bone,
                                  cuda=self.args.cuda)
        TPositives,FPositives = self.evaluate()
        return TPositives,FPositives
    
    def evaluate(self,):
        return self.evaluator.main()
    
    def inference(self,):
        pass