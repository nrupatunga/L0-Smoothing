"""
File: run_batch.py
Author: Nrupatunga
Email: nrupatunga.s@byjus.com
Github: https://github.com/nrupatunga
Description: run on batch of images
"""
import os
from pathlib import Path

import cv2
import numpy as np
from imutils import paths
from tqdm import tqdm

from L0_Smoothing import L0Smoothing

root_dir = './images'
image_files = paths.list_images(root_dir)

out_dir = './output'

for i, img_path in tqdm(enumerate(image_files)):
    img = cv2.imread(img_path)
    S = L0Smoothing(img_path, param_lambda=0.01).run()
    S = np.squeeze(S)
    S = np.clip(S, 0, 1)
    S = S * 255
    out = S.astype(np.uint8)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    out = np.hstack((img, out))

    out_path = os.path.join(out_dir, Path(img_path).name)
    cv2.imwrite(out_path, out)
