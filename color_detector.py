#!/usr/bin/env python3
import cv2
import numpy as np
from time import sleep
import os


if 'N_SPLITS' in os.environ:
    N_SPLITS = int(os.environ['N_SPLITS'])
else:
    raise RuntimeError('Environment variable N_SPLITS not defined')

print('Detecting color in %d equally sized horizontal sections' % N_SPLITS)


def findDominantColor(img):

    # Simple averaging RGB
    mean_BGR = np.sum(img, axis=(0,1)) / (img.shape[0]*img.shape[1])
    return '[{}, {}, {}]'.format(int(mean_BGR[0]), int(mean_BGR[1]), int(mean_BGR[2]))


cap = cv2.VideoCapture('/home/mike/duckietown/RH3/driving_straight_line.mp4') # For testing
# cap = cv2.VideoCapture(2) 

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        print('Frame read correctly, detecting colors')
        rows = frame.shape[0]
        drow = rows // N_SPLITS
        diff = rows - N_SPLITS*drow
        for i in range(N_SPLITS):
            start = i*drow
            end = (i+1)*drow + ((i+2)*drow > rows)*diff
            color = findDominantColor( frame[start:end, :] )
            print('In section %d the color is mostly %s' % (i+1, color))
    else:
        print('Frame not read correctly')


    #Put here your code!
    # You can now treat output as a normal numpy array
    # Do your magic here

    sleep(1)