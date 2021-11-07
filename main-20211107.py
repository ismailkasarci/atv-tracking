from vidgear.gears import CamGear
from vidgear.gears import VideoGear
import cv2
from tracker import *
import pygame
import numpy as np
import sys

tracker = EuclideanDistTracker()

# stream = CamGear(source="rtsp://admin:Admin1234@192.168.1.64:554/live").start()
stream = VideoGear(source="./recs/192.168.1.64_01_20211024150610309.mp4").start()

object_detector = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=80)

CAM_RES_FACTOR = 1
CAM_WIDTH = 480 * CAM_RES_FACTOR
CAM_HEIGHT = 270 * CAM_RES_FACTOR

SCREEN_FACTOR = 0.5
SCREEN_WIDTH = 3072 * SCREEN_FACTOR
SCREEN_HEIGHT = 766 * SCREEN_FACTOR

bg = stream.read()
bg = cv2.resize(bg, (CAM_WIDTH, CAM_HEIGHT))

takeBg = 0

while True:

    frame = stream.read()

    if frame is None:
        break

    frame = cv2.resize(frame, (CAM_WIDTH, CAM_HEIGHT))

    if takeBg == 1:
        bg = frame
        takeBg = 0

    fgMask = object_detector.apply(frame)

    diff = cv2.subtract(frame, bg)
    diff[abs(diff) < 30.0] = 0
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    cv2.imshow("diff", diff)

    kernel = np.ones((2, 2), np.uint8)

    fgMask = cv2.erode(fgMask, kernel, iterations=3)
    fgMask = cv2.dilate(fgMask, kernel, iterations=3)

    fgMask[np.abs(fgMask) < 100] = 0

    contours, _ = cv2.findContours(diff, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 300:
            # cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)

            detections.append([x, y, w, h])

    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(
            frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2
        )
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Frame", frame)
    cv2.imshow("FG Mask", fgMask)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif ord("e") == key:
        takeBg = 1

cv2.destroyAllWindows()

stream.stop()
