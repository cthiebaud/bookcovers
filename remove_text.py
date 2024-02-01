#!/usr/bin/env python3

import glob
import os
import matplotlib.pyplot as plt
import keras_ocr
from PIL import Image
import cv2
import math
import numpy as np
import tensorflow as tf

# Suppress TensorFlow deprecation warnings
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# https://towardsdatascience.com/remove-text-from-images-using-cv2-and-keras-ocr-24e7612ae4f4
# https://stackoverflow.com/a/53516832/1070215
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)
    return (x_mid, y_mid)

pipeline = keras_ocr.pipeline.Pipeline()

def inpaint_text(img_path, pipeline):
    # read image
    img = keras_ocr.tools.read(img_path)
    # generate (word, box) tuples 
    prediction_groups = pipeline.recognize([img])
    mask = np.zeros(img.shape[:2], dtype="uint8")
    
    for box in prediction_groups[0]:
        x0, y0 = box[1][0]
        x1, y1 = box[1][1] 
        x2, y2 = box[1][2]
        x3, y3 = box[1][3] 
        
        x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
        x_mid1, y_mid1 = midpoint(x0, y0, x3, y3)
        
        thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))
        
        cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255, thickness)
        
    img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
                 
    return img, mask

def save_with_alpha0(img_path, img_rgb, new_name):
    # Load the original image with alpha channel
    original_img = Image.open(img_path).convert("RGBA")

    # Extract alpha channel from the original image
    alpha_channel = np.array(original_img)[:, :, 3]

    # Check if the sizes are different
    if img_rgb.shape[:2] != (original_img.height, original_img.width):
        # Resize img_rgb to match the dimensions of the original image
        img_rgb = cv2.resize(img_rgb, (original_img.width, original_img.height))

    # Ensure both images have the same mode
    if original_img.mode != 'RGBA':
        original_img = original_img.convert('RGBA')

    # Merge RGB and alpha channels using numpy
    merged_image = np.dstack((img_rgb, alpha_channel))
    
    # Save the result
    Image.fromarray(merged_image, 'RGBA').save(new_name)

def save_with_alpha(img_path, img_rgb, new_name):
    # Load the original image with alpha channel
    original_img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

    # Extract alpha channel from the original image
    alpha_channel = original_img[:, :, 3]

    # Check if the sizes are different
    if img_rgb.shape[:2] != (original_img.shape[0], original_img.shape[1]):
        # Resize img_rgb to match the dimensions of the original image
        img_rgb = cv2.resize(img_rgb, (original_img.shape[1], original_img.shape[0]))

    # Merge RGB and alpha channels using numpy
    merged_image = np.dstack((img_rgb, alpha_channel))

    # Save the result using OpenCV
    cv2.imwrite(new_name, merged_image)


extensions = ['jpg', 'jpeg', 'webp', 'png']

for ext in extensions:
    for filename2 in glob.iglob('covers/*.' + ext, recursive=True):
        basename = os.path.basename(filename2)
        newName = f"covers-no-text/Z_{basename}"
        
        if not os.path.isfile(newName):
            print(f"\n{basename}")

            new_image, _ = inpaint_text(filename2, pipeline)
            img_rgb = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)

            if ext.lower() == 'png':
                # Save with separate alpha channel
                save_with_alpha(filename2, img_rgb, newName)
            else:
                cv2.imwrite(newName, img_rgb)
                
            print(newName)
