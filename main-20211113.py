from threading import current_thread
from vidgear.gears import CamGear
from vidgear.gears import VideoGear
import cv2
from tracker import *
import pygame
import numpy as np
import sys


class GSprite:
    def __init__(self):
        self.index = 0
        self.len = 10

    def update(self):
        self.index += 1
        if self.index >= self.len:
            self.index = 0


tracker = EuclideanDistTracker()

# stream = CamGear(source="rtsp://admin:Admin1234@192.168.1.64:554/live").start()
stream = VideoGear(source="./recs/11.mp4").start()

object_detector = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=80)

CAM_RES_FACTOR = 1
CAM_WIDTH = 480 * CAM_RES_FACTOR
CAM_HEIGHT = 270 * CAM_RES_FACTOR

SCREEN_FACTOR = 0.5
SCREEN_WIDTH = 3072 * SCREEN_FACTOR
SCREEN_HEIGHT = 766 * SCREEN_FACTOR

CAM_TO_SCREEN_FACTOR = SCREEN_WIDTH / CAM_WIDTH

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tracking")
bg_img = pygame.image.load("./assets/bg.png").convert_alpha()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
glow_img = pygame.image.load("./assets/glow.png").convert_alpha()
glow_img = pygame.transform.scale(glow_img, (100, SCREEN_HEIGHT))

current_sprite = 0
total_sprite = 10
sprite_frames = []
for i in range(1, 11):
    sprite_frames.append(
        pygame.image.load("./assets/glow-sequence/g-" + str(i) + ".png").convert_alpha()
    )

while True:

    frame = stream.read()

    if frame is None:
        break

    frame = cv2.resize(frame, (CAM_WIDTH, CAM_HEIGHT))

    fgMask = object_detector.apply(frame)

    kernel = np.ones((1, 1), np.uint8)

    # fgMask = cv2.erode(fgMask, kernel, iterations=3)
    # fgMask = cv2.dilate(fgMask, kernel, iterations=3)

    fgMask[np.abs(fgMask) < 100] = 0

    contours, _ = cv2.findContours(fgMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 300:
            # cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)

            detections.append([x, y, w, h])

    boxes_ids = tracker.update(detections)

    screen.fill((0, 0, 0))

    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(
            frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2
        )
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # screen.blit(glow_img, (x * CAM_TO_SCREEN_FACTOR, 0))
        screen.blit(sprite_frames[current_sprite], (x * CAM_TO_SCREEN_FACTOR, 0))

    current_sprite += 1
    if current_sprite == total_sprite:
        current_sprite = 0

    screen.blit(bg_img, (0, 0))

    cv2.imshow("Frame", frame)
    cv2.imshow("FG Mask", fgMask)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    pygame.display.flip()
    clock.tick(60)

cv2.destroyAllWindows()

stream.stop()
