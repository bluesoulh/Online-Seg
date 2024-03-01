import numpy as np
import matplotlib.pyplot as plt
from mmseg.apis import init_model,inference_model,show_result_pyplot
import cv2

def perform_semantic_segmentation(input_path,filename):
    # config配置文件
    config_file = 'test10 dmnet.py' #训练文件路径
    # 权重文件
    checkpoint_file = 'iter_36800.pth'#模型路径
    device = 'cuda:0'#使用显卡预测
    model = init_model(config_file, checkpoint_file, device=device)
    # 载入图像
    img_path = input_path
    img_bgr = cv2.imread(img_path)
    # 语义分割预测
    result = inference_model(model, img_bgr)
    pred_mask = result.pred_sem_seg.data[0].cpu().numpy()
    # 和原图并排显示
    plt.figure(figsize=(14, 8))
    plt.subplot(1, 2, 1)
    plt.imshow(img_bgr[:, :, ::-1])
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(img_bgr[:, :, ::-1])
    plt.imshow(pred_mask, alpha=0.6)
    plt.axis('off')
    plt.savefig('static/segm_result_images/{}'.format(filename))#保存路径，与原图同名