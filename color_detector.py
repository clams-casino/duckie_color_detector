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


def findDominantColor(img_hsv):
    BLACK_THRESHOLD = 36
    SAT_THRESHOLD = 21
    WHITE_THRESHOLD = 165
    color_counter = {'white':0, 'black':0, 'gray':0,
                     'red':0, 'orange':0, 'yellow':0, 'green':0,
                     'cyan':0, 'blue':0,'magenta':0, 'pink':0}
    
    for y in range(img_hsv.shape[0]):
        for x in range(img_hsv.shape[1]):
            # print(img_hsv[y,x])
            hue = img_hsv[y,x][0]
            sat = img_hsv[y,x][1]
            value = img_hsv[y,x][2]
            if value < BLACK_THRESHOLD:
                color_counter['black'] += 1
                
            else:
                if sat < SAT_THRESHOLD:
                    if value < WHITE_THRESHOLD:
                        color_counter['gray'] +=1
                    else:
                        color_counter['white'] += 1
                
                else:
                    if 0 <= hue < 20 or 340 <= hue <= 360:
                        color_counter['red'] += 1
                    elif 20 <= hue < 40:
                        color_counter['orange']  += 1
                    elif 40 <= hue < 70:
                        color_counter['yellow'] += 1
                    elif 70 <= hue < 160:
                        color_counter['green'] += 1
                    elif 160 <= hue < 190:
                        color_counter['cyan'] += 1
                    elif 190 <= hue < 260:
                        color_counter['blue'] += 1
                    elif 260 <= hue < 320:
                        color_counter['magenta'] += 1
                    else:
                        color_counter['pink'] += 1

    return sorted(color_counter.items(), key=lambda x:x[1], reverse=True)[0][0]



# cap = cv2.VideoCapture('/home/mike/duckietown/RH3/driving_straight_line.mp4') # For testing
cap = cv2.VideoCapture(2) 

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
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

    sleep(1)