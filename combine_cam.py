import cv2 
import numpy as np


cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)



while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    height1, width1, _ = frame1.shape
    height2, width2, _ = frame2.shape
    # print(width1, height1, width2, height2)

    frame1 = cv2.flip(frame1, 1)
    frame2 = cv2.flip(frame2, 1)
    
    vis = np.concatenate((frame2, frame1), axis=1)

    cv2.imshow("Combine", vis)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()