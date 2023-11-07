import sys
import os
import datetime
import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision.models import (resnet18,resnet34,resnet50,resnet101,resnet152,inception_v3,mobilenet_v2,mobilenet_v3_large,shufflenet_v2_x1_5)

from .utils.callbacks import LossHistory, EvalCallback
from .utils.dataloader import DataGenerator, detection_collate
from .utils.utils import (download_weights, get_classes, get_lr_scheduler,Model,
                    set_optimizer_lr, show_config, weights_init, MultiClassFocalLossWithAlpha)
from .utils.utils_fit import fit_one_epoch

def main(args):
    Cuda          = args.cuda
    distributed     = args.distributed
    sync_bn        = distributed 
    fp16          = args.fp16
    classes_path    = args.class_file
    input_shape     = args.input_size
    backbone       = args.back_bone
    backbone_map     = {'resnet18':resnet18, 'resnet34':resnet34, 'resnet50':resnet50, 'resnet101':resnet101, 
                        'resnet152':resnet152,'inception_v3':inception_v3, 'mobilenet_v2':mobilenet_v2, 
                        'mobilenet_v3':mobilenet_v3_large, 'shufflenet_v2':shufflenet_v2_x1_5}
    pretrained      = True
    model_path      = args.model_path

    Init_Epoch      = args.init_epoch
    Freeze_Epoch     = args.freeze_epoch
    Freeze_batch_size  = args.freeze_batch_size
    UnFreeze_Epoch    = args.unfreeze_epoch
    Unfreeze_batch_size = args.unfreeze_batch_size
    Freeze_Train     = args.freeze_train
    
    Init_lr        = args.init_lr
    Min_lr         = args.min_lr
    
    optimizer_type    = args.optimizer
    momentum        = args.momentum
    weight_decay     = args.weight_decay # adam:0
    
    lr_decay_type    = args.lr_decay_type
    save_period      = args.save_period
    save_dir        = args.save_dir
    num_workers      = args.num_worker
    eval_flag       = True
    eval_period      = 1
    
    train_annotation_path   = args.train_file
    test_annotation_path    = args.val_file
    model_name           = args.model_name
    time_str            = datetime.datetime.strftime(datetime.datetime.now(),'%Y_%m_%d_%H_%M_%S')
    model_name          = args.model_name if args.model_name else str(time_str)
    log_dir             = os.path.join(save_dir,f'log/loss_{model_name}')
    checkpoint_dir      = os.path.join(save_dir,f'checkpoint/{model_name}')
    os.makedirs(checkpoint_dir, exist_ok=True)
#     os.environ['CUDA_VISIBLE_DEVICE'] = '0'
    ngpus_per_node  = torch.cuda.device_count()
    if distributed:
        dist.init_process_group(backend="nccl")
        local_rank  = int(os.environ["LOCAL_RANK"])
        rank      = int(os.environ["RANK"])
        device     = torch.device("cuda", local_rank)
        if local_rank == 0:
            print(f"[{os.getpid()}] (rank = {rank}, local_rank = {local_rank}) training...")
            print("Gpu Device Count : ", ngpus_per_node)
    else:
        device     = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        local_rank  = 0
        rank      = 0

    class_names, num_classes = get_classes(classes_path)
    focal_loss_multicls = MultiClassFocalLossWithAlpha(alpha=[1]*num_classes, device=device)
#     if not 'shuffle' in backbone:
#         model = backbone_map[backbone](pretrained=True)
#     else:
#         model = backbone_map[backbone](pretrained=False)
#         if model_path != '':
#             model_dict      = model.state_dict()
#             pretrained_dict = torch.load(model_path, map_location = device)
#             load_key, no_load_key, temp_dict = [], [], {}
#             for k, v in pretrained_dict.items():
#                 if k in model_dict.keys() and np.shape(model_dict[k]) == np.shape(v):
#                     temp_dict[k] = v
#                     load_key.append(k)
#                 else:
#                     no_load_key.append(k)
#             model_dict.update(temp_dict)
#             model.load_state_dict(model_dict)
#             if local_rank == 0:
#                 print("\nSuccessful Load Key:", str(load_key)[:500], "……\nSuccessful Load Key Num:", len(load_key))
#                 print("\nFail To Load Key:", str(no_load_key)[:500], "……\nFail To Load Key num:", len(no_load_key))
    model = backbone_map[backbone](pretrained=True)
    if 'resnet' in backbone:
        fc_inputs = model.fc.in_features
        model.fc = nn.Linear(fc_inputs, num_classes)
    elif 'inception' in backbone:
        model.aux_logits = False
        fc_inputs = model.fc.in_features
        model.fc = nn.Linear(fc_inputs, num_classes)
    elif 'vit' in backbone:
        head_inputs = model.heads.head.in_features
        model.heads.head = nn.Linear(head_inputs, num_classes)
    elif 'swin' in backbone:
        head_inputs = model.head.in_features
        model.head = nn.Linear(head_inputs, num_classes)
    elif 'mobile' in backbone:
        fc_inputs = model.classifier[-1].in_features
        model.classifier[-1] = nn.Linear(fc_inputs, num_classes)
#         model.classifier = nn.Sequential(nn.Dropout(0.2),nn.Linear(in_features=1280,out_features=num_classes,bias=True))
    elif 'shuffle' in backbone:
        fc_inputs = model.fc.in_features
        model.fc = nn.Linear(fc_inputs, num_classes)
        
    if local_rank == 0:
        loss_history = LossHistory(log_dir, model, input_shape=input_shape)
    else:
        loss_history = None
        
    if fp16:
        from torch.cuda.amp import GradScaler as GradScaler
        scaler = GradScaler()
    else:
        scaler = None

    model_train     = model.train()
    if sync_bn and ngpus_per_node > 1 and distributed:
        model_train = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model_train)
    elif sync_bn:
        print("Sync_bn is not support in one gpu or not distributed.")

    if Cuda:
        if distributed:
            model_train = model_train.cuda(local_rank)
            model_train = torch.nn.parallel.DistributedDataParallel(model_train, device_ids=[local_rank], find_unused_parameters=True)
        else:
            model_train = torch.nn.DataParallel(model)
            cudnn.benchmark = True
            model_train = model_train.cuda()
        
    with open(train_annotation_path, encoding='utf-8') as f:
        train_lines = f.readlines()
    with open(test_annotation_path, encoding='utf-8') as f:
        val_lines   = f.readlines()
        val_lines   = [item.strip('\n') for item in val_lines]
    num_train   = len(train_lines)
    num_val    = len(val_lines)
    np.random.seed(10101)
    np.random.shuffle(train_lines)
    np.random.seed(None)
    
    if local_rank == 0:
        show_config(
            num_classes = num_classes, backbone = backbone, input_shape = input_shape, \
            Init_Epoch = Init_Epoch, Freeze_Epoch = Freeze_Epoch, UnFreeze_Epoch = UnFreeze_Epoch, Freeze_batch_size = Freeze_batch_size,\
            Unfreeze_batch_size = Unfreeze_batch_size, Freeze_Train = Freeze_Train, \
            Init_lr = Init_lr, Min_lr = Min_lr, optimizer_type = optimizer_type, momentum = momentum, lr_decay_type = lr_decay_type, \
            save_period = save_period, model_name = model_name, num_workers = num_workers, num_train = num_train, num_val = num_val
        )

    total_step  = num_train // Unfreeze_batch_size * UnFreeze_Epoch
    if True:
        UnFreeze_flag = False
        if Freeze_Train:
            for name, parameter in model.named_parameters():
                if not ('fc' in name or 'head' in name or 'classifier' in name):
                     parameter.requires_grad = False
        batch_size = Freeze_batch_size if Freeze_Train else Unfreeze_batch_size
        nbs             = 64
        lr_limit_max    = 1e-3 if optimizer_type == 'adam' else 1e-1
        lr_limit_min    = 1e-4 if optimizer_type == 'adam' else 5e-4
        if 'vit' in backbone or 'swin' in backbone:
            nbs             = 256
            lr_limit_max    = 1e-3 if optimizer_type == 'adam' else 1e-1
            lr_limit_min    = 1e-5 if optimizer_type == 'adam' else 5e-4
        Init_lr_fit     = min(max(batch_size / nbs * Init_lr, lr_limit_min), lr_limit_max)
        Min_lr_fit      = min(max(batch_size / nbs * Min_lr, lr_limit_min * 1e-2), lr_limit_max * 1e-2)
        Init_lr_fit     = Init_lr
        Min_lr_fit      = Min_lr
        
        optimizer = {
            'adam'  : optim.Adam(model_train.parameters(), Init_lr_fit, betas = (momentum, 0.999), weight_decay=weight_decay),
            'adamw'  : optim.AdamW(model_train.parameters(), Init_lr_fit, betas = (momentum, 0.999), weight_decay=weight_decay),
            'sgd'   : optim.SGD(model_train.parameters(), Init_lr_fit, momentum = momentum, nesterov=True)
        }[optimizer_type]
        
        lr_scheduler_func = get_lr_scheduler(lr_decay_type, Init_lr_fit, Min_lr_fit, UnFreeze_Epoch)
        
        epoch_step      = num_train // batch_size
        epoch_step_val  = num_val // batch_size

        train_dataset   = DataGenerator(train_lines, input_shape, num_classes, True, True)
        val_dataset     = DataGenerator(val_lines, input_shape, num_classes, False, True)
        
        if distributed:
            train_sampler   = torch.utils.data.distributed.DistributedSampler(train_dataset, shuffle=True,)
            val_sampler     = torch.utils.data.distributed.DistributedSampler(val_dataset, shuffle=False,)
            batch_size      = batch_size // ngpus_per_node
            shuffle         = False
        else:
            train_sampler   = None
            val_sampler     = None
            shuffle         = True
            
        gen             = DataLoader(train_dataset, shuffle=shuffle, batch_size=batch_size, num_workers=num_workers, pin_memory=True, 
                                drop_last=True, collate_fn=detection_collate, sampler=train_sampler)
        gen_val         = DataLoader(val_dataset, shuffle=shuffle, batch_size=batch_size, num_workers=num_workers, pin_memory=True,
                                drop_last=True, collate_fn=detection_collate, sampler=val_sampler)
        
        eval_callback   = EvalCallback(model, input_shape, class_names, num_classes, val_lines, log_dir, Cuda, \
                                            eval_flag=eval_flag, period=eval_period)
        for epoch in range(Init_Epoch, UnFreeze_Epoch):
            if epoch >= Freeze_Epoch and not UnFreeze_flag and Freeze_Train:
                batch_size = Unfreeze_batch_size
                nbs             = 64
                lr_limit_max    = 1e-3 if 'adam' in optimizer_type else 1e-1
                lr_limit_min    = 1e-4 if 'adam' in optimizer_type else 5e-4
                if 'vit' in backbone or 'swin' in backbone:
                    nbs             = 256
                    lr_limit_max    = 1e-3 
                    lr_limit_min    = 1e-5 
                Init_lr_fit     = min(max(batch_size / nbs * Init_lr, lr_limit_min), lr_limit_max)
                Min_lr_fit      = min(max(batch_size / nbs * Min_lr, lr_limit_min * 1e-2), lr_limit_max * 1e-2)
                Init_lr_fit     = Init_lr
                Min_lr_fit      = Min_lr
                lr_scheduler_func = get_lr_scheduler(lr_decay_type, Init_lr_fit, Min_lr_fit, UnFreeze_Epoch)
                
                if epoch == Freeze_Epoch:
                    for name, parameter in model.named_parameters():
                        if not ('fc' in name or 'head' in name or 'classifier' in name):
                             parameter.requires_grad = True

                epoch_step      = num_train // batch_size
                epoch_step_val  = num_val // batch_size

                if epoch_step == 0 or epoch_step_val == 0:
                    raise ValueError("数据集过小，无法继续进行训练，请扩充数据集。")

                if distributed:
                    batch_size = batch_size // ngpus_per_node

                gen     = DataLoader(train_dataset, shuffle=shuffle, batch_size=batch_size, num_workers=num_workers, \
                             pin_memory=True,drop_last=True, collate_fn=detection_collate, sampler=train_sampler)
                gen_val  = DataLoader(val_dataset, shuffle=shuffle, batch_size=batch_size, num_workers=num_workers, \
                             pin_memory=True, drop_last=True, collate_fn=detection_collate, sampler=val_sampler)

                UnFreeze_flag = True

            if distributed:
                train_sampler.set_epoch(epoch)
                
            set_optimizer_lr(optimizer, lr_scheduler_func, epoch)
            
            fit_one_epoch(model_train, model, loss_history, eval_callback, optimizer, epoch, epoch_step, epoch_step_val, \
                      gen, gen_val, UnFreeze_Epoch, Cuda, fp16, scaler, save_period, checkpoint_dir, local_rank,focal_loss=focal_loss_multicls)

#         if local_rank == 0:
#             loss_history.writer.close()
            
            
def display_args(args):
    print('--------args----------')
    for k in list(vars(args).keys()):
        print('%s: %s' % (k, vars(args)[k]))
    print('--------args----------\n')


if __name__ == "__main__":
    from src import BaseTrain
    #-----------------------------------------------------
    #  base_config and model_config required from input
    #-----------------------------------------------------
    #base_config, model_config
    #mp.set_start_method("spawn")
    args = BaseTrain().parse_args()
    main(args)
