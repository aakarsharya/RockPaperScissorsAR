"""
Create vector representation + labels for images
Image augmentation to produce larger dataset
"""
import os 
import sys
import cv2
import numpy as np
import pandas as pd
import time

hands = {'rock': 0, 'paper': 1, 'scissors': 2, 'other': 3}

def oneHotEncode(labels, n_classes=4):
    return np.eye(n_classes, dtype=int)[labels]

# image data augmentation
def horizontalFlip(img):
    return cv2.flip(img, 1)

def verticalFlip(img):
    return cv2.flip(img, 0)

def grayScale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def rotate(img, angle):
    return cv2.rotate(img, angle)

def augment():
    for hand in hands.keys():
        for filename in os.listdir(hand):
            img = cv2.imread(os.path.join(hand, filename))
            filename = filename.split('.')[0]
            cv2.imwrite(filename=os.path.join(hand, "{}_hflip.jpg".format(filename)), img=horizontalFlip(img))
            cv2.imwrite(filename=os.path.join(hand, "{}_vflip.jpg".format(filename)), img=verticalFlip(img))
            cv2.imwrite(filename=os.path.join(hand, "{}_grayscale.jpg".format(filename)), img=grayScale(img))
            cv2.imwrite(filename=os.path.join(hand, "{0}_rotate90cw.jpg".format(filename)), 
                img=rotate(img, cv2.ROTATE_90_CLOCKWISE))
            cv2.imwrite(filename=os.path.join(hand, "{0}_rotate90ccw.jpg".format(filename)), 
                img=rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))

# label images
def preprocess():
    start = time.time()
    df = pd.DataFrame(columns=['image', 'label'])
    for hand in hands.keys():
        if hand == 'other':
            continue
        for filename in os.listdir(hand):
            img = cv2.imread(os.path.join(hand, filename))
            img = cv2.resize(img, (227, 227))
            df = df.append({'image': img, 'label': hands[hand]}, ignore_index=True)
    end = time.time()
    print("time taken for preprocessing and labelling", end - start)
    df['label'] = oneHotEncode(df['label'].astype(int))
    return df

# df = preprocess()
# df.to_csv('imageData.csv')
augment()







