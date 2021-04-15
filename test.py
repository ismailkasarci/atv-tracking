import numpy as np
import cv2 as cv
import time


running = True;

cap1 = cv.VideoCapture(0, cv.CAP_DSHOW)
cap2 = cv.VideoCapture(1, cv.CAP_DSHOW)

cap1.set(cv.CAP_PROP_FRAME_WIDTH, 320)
cap1.set(cv.CAP_PROP_FRAME_HEIGHT, 240)

cap2.set(cv.CAP_PROP_FRAME_WIDTH, 320)
cap2.set(cv.CAP_PROP_FRAME_HEIGHT, 240)



img1 = cv.imread('./assets/s1.jpg')
img2 = cv.imread('./assets/s2.jpg')
images = []
#images.append(img1)
#images.append(img2)

def main():
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    frame1 = cv.flip(frame1, 1)
    frame2 = cv.flip(frame2, 1)

    images.append(img1)
    images.append(img2)

    stitcher = cv.Stitcher.create()
    start = time.perf_counter()
    status, pano = stitcher.stitch(images)
    finish = time.perf_counter()
    print(f'Toplam {round(finish-start, 2)} saniye surdu')

    images.clear()

    if status != cv.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
    else:
        cv.imshow('Stitch', pano)

if __name__ == '__main__':
    while running:
        main()
        key = cv.waitKey(30)
        if key == 27:
            cv.destroyAllWindows()
            break
    
    