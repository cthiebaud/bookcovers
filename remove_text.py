import glob
import os
import matplotlib.pyplot as plt
import keras_ocr
import cv2
import math
import numpy as np

## https://towardsdatascience.com/remove-text-from-images-using-cv2-and-keras-ocr-24e7612ae4f4

## https://stackoverflow.com/a/53516832/1070215
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
        x_mid1, y_mi1 = midpoint(x0, y0, x3, y3)
        
        thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))
        
        cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255,    
        thickness)
        img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
                 
    return(img)

extensions = ['jpg', 'jpeg', 'webp', 'png']
for ext in extensions:
    # for filename2 in glob.iglob('thumbs/*.'+ext, recursive=True):
    for filename2 in glob.iglob('covers/*.'+ext, recursive=True):

        basename = os.path.basename(filename2)
        newName = f"covers-no-text/Z_{basename}"
        if not os.path.isfile(newName):

            new_image = inpaint_text(filename2, pipeline)
            img_rgb = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)

            cv2.imwrite(newName,img_rgb)
            print(newName)
                    