from threading import Thread
import numpy as np
import cv2
import pygame
from tracker import *

CAM_WIDTH = 1280
CAM_HEIGHT = 720
WIDTH = 1920
HEIGHT = 1080


class VideoGet:

    def __init__(self):
        self.stream = cv2.VideoCapture(
            'rtsp://admin:Admin1234@192.168.1.64:554/live')
        #self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        #self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=(), daemon=True).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stream.release()
        self.stopped = True


tracker = EuclideanDistTracker()


object_detector = cv2.createBackgroundSubtractorMOG2(
    history=100, varThreshold=40)

video_getter = VideoGet().start()

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
glow_img = pygame.image.load('./assets/glow_star.png').convert_alpha()


while True:

    frame = video_getter.frame
    roi = frame[0:, 0:]

    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 1000:
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)

            detections.append([x, y, w, h])

    screen.fill((0, 0, 0))

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y - 15),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if(y > 0 and y < 200):
            if(x > 200 and x < 1000):
                nx = ((x - 200) / 800.0) * WIDTH
                screen.blit(glow_img, (nx, 400))
        elif(y >= 200 and y < 400):
            if(x > 100 and x < 1000):
                nx = ((x - 100) / 900.0) * WIDTH
                screen.blit(glow_img, (nx, 400))
        if(y >= 400 and y < 600):
            if(x > 0 and x < 1200):
                nx = ((x - 0) / 1200.0) * WIDTH
                screen.blit(glow_img, (nx, 400))

    cv2.imshow("Roi", roi)
    cv2.imshow("Mask", mask)

    pygame.display.flip()
    clock.tick(60)

    key = cv2.waitKey(10)
    if key == 27:
        break

video_getter.stop()
cv2.destroyAllWindows()

