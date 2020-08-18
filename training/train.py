import os
import sys
import cv2
import time
import numpy as np
import tensorflow as tf
from keras import Sequential
from keras.layers import Flatten, Dense, Dropout, Conv2D, MaxPooling2D
from keras.models import load_model
from sklearn.model_selection import train_test_split

hands = {'rock': 0, 'paper': 1, 'scissors': 2, 'other': 3}
augmentData = sys.argv[1]

def getHand(idx):
    for key, val in hands.items():
        if idx == val:
            return key

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

# Dataset augmentation
def augment():
    for hand in hands.keys():
        for filename in os.listdir(hand):
            img = cv2.imread(os.path.join(hand, filename))
            filename = filename.split('.')[0]
            cv2.imwrite(filename=os.path.join(hand, "{}_hflip.jpg".format(filename)), img=horizontalFlip(img))
            cv2.imwrite(filename=os.path.join(hand, "{}_vflip.jpg".format(filename)), img=verticalFlip(img))
            cv2.imwrite(filename=os.path.join(hand, "{}_grayscale.jpg".format(filename)), img=grayScale(img))
            cv2.imwrite(filename=os.path.join(hand, "{}_rotate90cw.jpg".format(filename)), 
                img=rotate(img, cv2.ROTATE_90_CLOCKWISE))
            cv2.imwrite(filename=os.path.join(hand, "{}_rotate90ccw.jpg".format(filename)), 
                img=rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))

class ConvNet(object):
    def __init__(self, dropout=0.5):
        self.model = Sequential()
        self.model.add(Conv2D(64, (3, 3), activation='relu', input_shape=(227,227,3)))
        self.model.add(MaxPooling2D(2,2))
        self.model.add(Conv2D(64, (3, 3), activation='relu'))
        self.model.add(MaxPooling2D(2,2))
        self.model.add(Conv2D(128, (3, 3), activation='relu'))
        self.model.add(MaxPooling2D(2,2))
        self.model.add(Conv2D(128, (3, 3), activation='relu'))
        self.model.add(MaxPooling2D(2,2))
        self.model.add(Flatten())
        self.model.add(Dropout(dropout))
        self.model.add(Dense(256, activation='relu'))
        self.model.add(Dense(4, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics='accuracy')

    def preprocess(self):
        start = time.time()
        images = []
        labels = []
        for hand in hands.keys():
            for filename in os.listdir(hand):
                img = cv2.imread(os.path.join(hand, filename))
                img = cv2.resize(img, (227, 227))
                images.append(img)
                labels.append(hands[hand])
        labels = oneHotEncode(labels)
        end = time.time()
        print("time taken for preprocessing and labelling", end - start)
        return np.array(images), labels

    def train(self, epochs=3, evaluate=False):
        images, labels = self.preprocess()
        Xtrain, Xtest, Ytrain, Ytest = train_test_split(images, labels, test_size=0.15, shuffle=True)
        history = self.model.fit(x=Xtrain, y=Ytrain, epochs=epochs)
        self.model.save(os.path.join("..", "rps_model.h5"))

    def load(self):
        self.model = load_model(os.path.join("..", "rps_model.h5"))

    def predict(self, img):
        prediction = self.model.predict(np.asarray([img]))
        return getHand(np.argmax(prediction))

if __name__ == "__main__":
    model = ConvNet()
    if augmentData == "augment":
        augment()
