import cv2
import numpy as np
from keras.models import load_model

cap = cv2.VideoCapture(0)
hands = {'rock': 0, 'paper': 1, 'scissors': 2, 'other': 3}
font = cv2.FONT_HERSHEY_PLAIN


