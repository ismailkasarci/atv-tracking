import cv2 
import numpy as np
# import pygame

cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)

print(cv2.__version__)

running = True
while running:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    #height1, width1, _ = frame1.shape
    #height2, width2, _ = frame2.shape
    #print(width1, height1, width2, height2)

    # frame_h = np.hstack((frame1, frame2)) # frame_v = np.vstack((frame, frame_t))
    vis = np.concatenate((frame2, frame1), axis=1)
    
    stitcher = cv2.Stitcher.create()
    images = []


    if ret1:
        images.append(frame1)
    if ret2:
        images.append(frame2)

    

    
    if ret1 and ret2:
        status, result = stitcher.stitch(images)

    images.clear()
    #cv2.imshow('title', vis)

    if cv2.waitKey(10) == 113: #Quit when you click q
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()