"""
File: run_batch.py
Author: Nrupatunga
Email: nrupatunga.s@byjus.com
Github: https://github.com/nrupatunga
Description: run on batch of images
"""
import glob
import os

import cv2
import numpy as np
from tqdm import tqdm
import time
import matplotlib.pyplot as plt

from L0Smoothing import L0Smoothing

root_dir = \
    '/home/nthere/2020/handwriting-ocr/data/REAL_DATA_JEROME/processed/test-org/'
image_files = glob.glob(os.path.join(root_dir, '**', '*.bmp'),
                        recursive=True)

out_dir = './REAL_DATA_JEROME'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for i, img_path in tqdm(enumerate(image_files)):
    img = cv2.imread(img_path, 0)
    fig, axs = plt.subplots(1, 2)
    n, _, _ = axs[0].hist(img.ravel() / 255, bins=256, range=(0.0, 0.5), fc='k', ec='k')
    ratio = sum(n) / (img.shape[0] * img.shape[1])

    start = time.time()
    S = L0Smoothing(img_path, param_lambda=ratio / 2).run()
    print('Time taken for one image: {}'.format(time.time() - start))
    S = np.squeeze(S)
    S = np.clip(S, 0, 1)
    S = S * 255
    S = S.astype(np.uint8)
    out = np.concatenate((img, S), axis=1)
    out_path = os.path.join(out_dir, str(i) + '.bmp')

    print('Ratio = {}'.format(ratio))
    axs[1].imshow(out)
    axs[0].axis('off')
    axs[1].axis('off')
    plt.draw()
    plt.waitforbuttonpress(0)
    plt.close()
    # cv2.imwrite(out_path, out)
