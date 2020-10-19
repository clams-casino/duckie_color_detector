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


def downscale(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def findDominantColor(img_hsv):
    BLACK_THRESHOLD = 50
    SAT_THRESHOLD = 50
    WHITE_THRESHOLD = 150
    color_counter = {'white':0, 'black':0, 'gray':0,
                     'red':0, 'orange':0, 'yellow':0, 'green':0,
                     'cyan':0, 'blue':0,'magenta':0, 'pink':0}
    
    for y in range(img_hsv.shape[0]):
        for x in range(img_hsv.shape[1]):
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
                    if 0 <= hue < 10 or 170 <= hue <= 180:
                        color_counter['red'] += 1
                    elif 10 <= hue < 20:
                        color_counter['orange']  += 1
                    elif 20 <= hue < 35:
                        color_counter['yellow'] += 1
                    elif 35 <= hue < 80:
                        color_counter['green'] += 1
                    elif 80 <= hue < 95:
                        color_counter['cyan'] += 1
                    elif 95 <= hue < 130:
                        color_counter['blue'] += 1
                    elif 130 <= hue < 160:
                        color_counter['magenta'] += 1
                    else:
                        color_counter['pink'] += 1

    return sorted(color_counter.items(), key=lambda x:x[1], reverse=True)[0][0]


cap = cv2.VideoCapture(2) 

while(True):
    # Capture frame-by-frame
    try:
        ret, frame = cap.read()
        frame = downscale(frame, 0.3)
        frame = cv2.GaussianBlur(frame, (1,1), 0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if ret:
            print('Frame read correctly, detecting colors')
            result = ''
            rows = frame.shape[0]
            drow = rows // N_SPLITS
            diff = rows - N_SPLITS*drow
            for i in range(N_SPLITS):
                start = i*drow
                end = (i+1)*drow + ((i+2)*drow > rows)*diff
                color = findDominantColor( frame[start:end, frame.shape[1]//3:-frame.shape[1]//3] )
                result += 'In section {} the color is mostly {}\n'.format(i+1, color)
            print(result)
        else:
            print('Frame not read correctly')

        sleep(1)

    except KeyboardInterrupt:
        break

print('Releasing video capture')
cap.release()