class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict):
            value = DotDict(value)
        return value
    
class base():
    model = DotDict()
    model.default = 'resnet18'
    model.optimizer = 'adamw'
    
    train = DotDict()
    train.cuda = False
    train.distributed = False
    train.fp16 = False
    train.num_worker = 0
    train.class_file = 'dataset/pork/classes.txt'
    train.train_file = 'dataset/pork/train.txt'
    train.val_file = 'dataset/pork/val.txt'
    train.freeze_train = True
    train.init_epoch = 0
    train.freeze_epoch = 5
    train.freeze_batch_size = 32
    train.unfreeze_epoch = 500
    train.unfreeze_batch_size = 16
    
    train.save_period = 1
    train.momentum = 0.9
    train.lr_decay_type = 'cos'
    
    train.sgd = DotDict()
    train.sgd.init_lr = 1e-3
    train.sgd.min_lr = 1e-5
    train.sgd.weight_decay = 5e-4
    
    train.adam = DotDict()
    train.adam.init_lr = 1e-4
    train.adam.min_lr = 1e-6
    train.adam.weight_decay = 0
    
    train.adamw = DotDict()
    train.adamw.init_lr = 1e-4
    train.adamw.min_lr = 1e-6
    train.adamw.weight_decay = 1e-4
    
    evaluate = DotDict()
    evaluate.num_class = 13
    evaluate.max_box = 100
    evaluate.confidence = 0.5
    evaluate.nms_iou = 0.3
    
    augmentation = DotDict()
    augmentation.aug_ratio = 0.7
    augmentation.mosaic = True
    augmentation.mosaic_prob = 0.5
    augmentation.mixup = True
    augmentation.mixup_prob = 0.5
    
    confvariable = DotDict()
    confvariable.variables = {'wheel':1}
    
class resnet18(base):
    def __init__(self,):
        base.model.back_bone = 'resnet18'
        base.model.input_size = [224,224]
        base.model.model_path = None
        base.model.phi = None
    
class resnet34(base):
    def __init__(self,):
        base.model.back_bone = 'resnet34'
        base.model.input_size = [224,224]
        base.model.model_path = None
        base.model.phi = None
    
class resnet50(base):
    def __init__(self,):
        base.model.back_bone = 'resnet50'
        base.model.input_size = [256,256]
        base.model.model_path = None
        base.model.phi = None
    
class resnet101(base):
    def __init__(self,):
        base.model.back_bone = 'resnet101'
        base.model.input_size = [256,256]
        base.model.model_path = None
        base.model.phi = None
    
class resnet152(base):
    def __init__(self,):
        base.model.back_bone = 'resnet152'
        base.model.input_size = [256,256]
        base.model.model_path = None
        base.model.phi = None
    
class inception_v3(base):
    def __init__(self,):
        base.model.back_bone = 'inception_v3'
        base.model.input_size = [299,299]
        base.model.model_path = None
        base.model.phi = None

class mobilenet_v2(base):
    def __init__(self,):
        base.model.back_bone = 'mobilenet_v2'
        base.model.input_size = [256,256]
        base.model.model_path = None
        base.model.phi = None
    
class mobilenet_v3(base):
    def __init__(self,):
        base.model.back_bone = 'mobilenet_v3'
        base.model.input_size = [256,256]
        base.model.model_path = None
        base.model.phi = None
    
class shufflenet_v2(base):
    def __init__(self,):
        base.model.back_bone = 'shufflenet_v2'
        base.model.input_size = [256,256]
        base.model.model_path = None
        base.model.phi = None

    
model_registry = {
    'resnet18':resnet18,
    'resnet34':resnet34,
    'resnet50':resnet50,
    'resnet101':resnet101,
    'resnet152':resnet152,
    'inception_v3':inception_v3,
    'mobilenet_v2':mobilenet_v2,
    'mobilenet_v3':mobilenet_v3,
    'shufflenet_v2':shufflenet_v2
}
        