import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from threading import local

import torch
import torch.nn.functional as F
from torch import nn
from torcheval.metrics.functional import r2_score
from tqdm import tqdm

from src.utils.utils import get_lr


def fit_one_epoch(model_train, model, loss_history, eval_callback, optimizer, epoch, epoch_step, epoch_step_val, gen, gen_val, Epoch, cuda, fp16, scaler, save_period, save_dir, local_rank=0, focal_loss=False):
    total_loss      = 0
    total_accuracy_value1  = 0
    total_accuracy_value2  = 0
    total_accuracy_value3  = 0
    total_accuracy_value4  = 0

    val_loss        = 0
    total_r2_value1 = 0
    total_r2_value2 = 0
    total_r2_value3 = 0
    total_r2_value4 = 0
    val_accuracy    = 0
    
    if local_rank == 0:
        print('Start Train')
        pbar = tqdm(total=epoch_step,desc=f'Epoch {epoch + 1}/{Epoch}',postfix=dict,mininterval=0.3)
    model_train.train()
    for iteration, batch in enumerate(gen):
        if iteration >= epoch_step: 
            break
        images, targets = batch
        with torch.no_grad():
            if cuda:
                images  = images.cuda(local_rank)
                targets = targets.cuda(local_rank)
                
        #----------------------#
        #   清零梯度
        #----------------------#
        optimizer.zero_grad()
        if not fp16:
            #----------------------#
            #   前向传播
            #----------------------#
            out1,out2,out3,out4 = model_train(images)
            out2,out3,out4      = torch.flatten(out2),torch.flatten(out3),torch.flatten(out4)
            #----------------------#
            #   计算损失
            #----------------------#
            loss_value1  = nn.CrossEntropyLoss()(out1, targets[...,0])
            loss_value2  = nn.BCELoss()(out2, targets[...,1].type(torch.float32))
            loss_value3  = nn.BCELoss()(out3, targets[...,2].type(torch.float32))
            loss_value4  = nn.BCELoss()(out4, targets[...,3].type(torch.float32))
#             loss_value1.backward()
#             loss_value2.backward()
#             loss_value3.backward()
#             loss_value4.backward()
#             loss_value1 = nn.L1Loss()(outputs[...,0], targets[...,0])
#             loss_value2 = nn.L1Loss()(outputs[...,1], targets[...,1])
#             loss_value3 = nn.L1Loss()(outputs[...,2], targets[...,2])
#             loss_value4 = nn.L1Loss()(outputs[...,3], targets[...,3])
            train_loss = loss_value1+loss_value2+loss_value3+loss_value4
            train_loss.backward()
            optimizer.step()
        else:
            from torch.cuda.amp import autocast
            with autocast():
                #----------------------#
                #   前向传播
                #----------------------#
                outputs     = model_train(images)
                #----------------------#
                #   计算损失
                #----------------------#
#                 loss_value  = nn.CrossEntropyLoss()(outputs, targets)
                loss_value = nn.L1Loss()(outputs[...,1], targets[...,1])
            #----------------------#
            #   反向传播
            #----------------------#
            scaler.scale(loss_value).backward()
            scaler.step(optimizer)
            scaler.update()

        total_loss += loss_value1.item()+loss_value2.item()+loss_value3.item()+loss_value4.item()
        with torch.no_grad():
            accuracy_value1 = torch.mean((torch.argmax(out1, dim=-1) == targets[...,0]).type(torch.FloatTensor))
            accuracy_value2 = torch.mean((torch.round(out2) == targets[...,1]).type(torch.FloatTensor))
            accuracy_value3 = torch.mean((torch.round(out3) == targets[...,2]).type(torch.FloatTensor))
            accuracy_value4 = torch.mean((torch.round(out4) == targets[...,3]).type(torch.FloatTensor))
            total_accuracy_value1 += accuracy_value1.item()
            total_accuracy_value2 += accuracy_value2.item()
            total_accuracy_value3 += accuracy_value3.item()
            total_accuracy_value4 += accuracy_value4.item()
            
#             r2_value1       = r2_score(outputs[...,0], targets[...,0])
#             r2_value2       = r2_score(outputs[...,1], targets[...,1])
#             r2_value3       = r2_score(outputs[...,2], targets[...,2])
#             r2_value4       = r2_score(outputs[...,3], targets[...,3])
#             total_r2_value1 += r2_value1.item()
#             total_r2_value2 += r2_value2.item()
#             total_r2_value3 += r2_value3.item()
#             total_r2_value4 += r2_value4.item()

        if local_rank == 0:
            pbar.set_postfix(**{'total_loss': total_loss / (iteration + 1), 
                                'acc_1'  : total_accuracy_value1 / (iteration + 1), 
                                'acc_2'  : total_accuracy_value2/ (iteration + 1), 
                                'acc_3'  : total_accuracy_value3 / (iteration + 1), 
                                'acc_4'  : total_accuracy_value4 / (iteration + 1), 
                                'lr'        : get_lr(optimizer)})
            pbar.update(1)
    
    total_accuracy_value1  = 0
    total_accuracy_value2  = 0
    total_accuracy_value3  = 0
    total_accuracy_value4  = 0
    total_r2_value1 = 0
    total_r2_value2 = 0
    total_r2_value3 = 0
    total_r2_value4 = 0
    if local_rank == 0:
        pbar.close()
        print('Finish Train')
        print('Start Validation')
        pbar = tqdm(total=epoch_step_val, desc=f'Epoch {epoch + 1}/{Epoch}',postfix=dict,mininterval=0.3)
    model_train_eval = model_train.eval()
    model_train.eval()
    for iteration, batch in enumerate(gen_val):
        if iteration >= epoch_step_val:
            break
        images, targets = batch
        with torch.no_grad():
            if cuda:
                images  = images.cuda(local_rank)
                targets = targets.cuda(local_rank)

            optimizer.zero_grad()

            outputs     = model_train(images)
            loss_value1  = nn.CrossEntropyLoss()(out1, targets[...,0])
            loss_value2  = nn.BCELoss()(out2, targets[...,1].type(torch.float32))
            loss_value3  = nn.BCELoss()(out3, targets[...,2].type(torch.float32))
            loss_value4  = nn.BCELoss()(out4, targets[...,3].type(torch.float32))
#             loss_value1  = nn.L1Loss()(outputs[...,0], targets[...,0])
#             loss_value2  = nn.L1Loss()(outputs[...,1], targets[...,1])
#             loss_value3  = nn.L1Loss()(outputs[...,2], targets[...,2])
#             loss_value4  = nn.L1Loss()(outputs[...,3], targets[...,3])
            val_loss    += loss_value1.item()+loss_value2.item()+loss_value3.item()+loss_value4.item()

            accuracy_value1 = torch.mean((torch.argmax(out1, dim=-1) == targets[...,1]).type(torch.FloatTensor))
            accuracy_value2 = torch.mean((torch.round(out2) == targets[...,1]).type(torch.FloatTensor))
            accuracy_value3 = torch.mean((torch.round(out3) == targets[...,2]).type(torch.FloatTensor))
            accuracy_value4 = torch.mean((torch.round(out4) == targets[...,3]).type(torch.FloatTensor))
            total_accuracy_value1 += accuracy_value1.item()
            total_accuracy_value2 += accuracy_value2.item()
            total_accuracy_value3 += accuracy_value3.item()
            total_accuracy_value4 += accuracy_value4.item()
#             r2_value1       = r2_score(outputs[...,0], targets[...,0])
#             r2_value2       = r2_score(outputs[...,1], targets[...,1])
#             r2_value3       = r2_score(outputs[...,2], targets[...,2])
#             r2_value4       = r2_score(outputs[...,3], targets[...,3])
#             total_r2_value1 += r2_value1.item()
#             total_r2_value2 += r2_value2.item()
#             total_r2_value3 += r2_value3.item()
#             total_r2_value4 += r2_value4.item()
            
        if local_rank == 0:
            pbar.set_postfix(**{'total_loss': val_loss / (iteration + 1),
                                'acc_1'  : total_accuracy_value1 / (iteration + 1), 
                                'acc_2'  : total_accuracy_value2/ (iteration + 1), 
                                'acc_3'  : total_accuracy_value3 / (iteration + 1), 
                                'acc_4'  : total_accuracy_value4 / (iteration + 1), 
                                'lr'        : get_lr(optimizer)})
            pbar.update(1)
                
    if local_rank == 0:
        pbar.close()
        print('Finish Validation')
        loss_history.append_loss(epoch + 1, total_loss / epoch_step, val_loss / epoch_step_val)
#         loss_history.append_acc(val_accuracy)
        eval_callback.on_epoch_end(epoch+1, model_train_eval)
        print('Epoch:' + str(epoch + 1) + '/' + str(Epoch))
        print('Total Loss: %.3f || Val Loss: %.3f ' % (total_loss / epoch_step, val_loss / epoch_step_val))
        
        #-----------------------------------------------#
        #   保存权值
        #-----------------------------------------------#
#         if (epoch + 1) % save_period == 0 or epoch + 1 == Epoch:
#             torch.save(model.state_dict(), os.path.join(save_dir, "ep%03d-loss%.3f-val_loss%.3f.pth" % (epoch + 1, total_loss / epoch_step, val_loss / epoch_step_val)))

        if len(loss_history.val_loss) <= 1 or (val_loss / epoch_step_val) <= min(loss_history.val_loss):
            print('Save best model to best_epoch_weights.pth')
            torch.save(model.state_dict(), os.path.join('checkpoint', save_dir, "best_epoch_weights.pth"))
#         if val_accuracy >= max(loss_history.val_acc): 
#             print('Save best model to best_acc_weights.pth')
#             torch.save(model.state_dict(), os.path.join('checkpoint', save_dir, "best_acc_weights.pth"))
