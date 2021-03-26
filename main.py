import cv2
import numpy as np
import pygame
from tracker import *

WIDTH, HEIGHT = 1440, 810


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Tracking')

bg_img = pygame.image.load('./assets/ilkeler-duvari-hd.jpg')

glow_img = pygame.image.load('./assets/track-glow-1.png').convert_alpha()


# Create tracker object
tracker = EuclideanDistTracker()

cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(0, cv2.CAP_DSHOW)




# cv2.namedWindow('output',cv2.WINDOW_KEEPRATIO)
# cv2.setWindowProperty('output',cv2.WND_PROP_ASPECT_RATIO,cv2.WINDOW_KEEPRATIO)
# cv2.setWindowProperty('output',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=40)

blobs = []


running = True
while running:

    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    

    if not ret1:
        print("Kamera 1 den goruntu gelmiyor.")
        break
    if not ret2:
        print("Kamera 2 den goruntu gelmiyor.")
        break

    height1, width1, _ = frame1.shape
    height2, width2, _ = frame2.shape
    # print(width1, height1, width2, height2)

    frame1 = cv2.flip(frame1, 1)
    frame2 = cv2.flip(frame2, 1)
    frame = np.concatenate((frame1, frame2), axis=1)

    # Extract Region of interest
    roi = frame[0: , 0: ]

    # 1. Object Detection
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 5000:
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)


            detections.append([x, y, w, h])

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)

    screen.fill((0, 0, 0))
    screen.blit(bg_img, (0, 0))

    for box_id in boxes_ids:
        # print(box_id)
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (100, 54, 255), 3)
        # cv2.rectangle(bg_img, (x, y), (x + w, y + h), (255, 255, 255), -1)
        
    
        found = False
        for blobItem in blobs:
            bx, by, bw, bh, bid, bf = blobItem
            if id == bid:
                found = True
                blobItem[0] += (x - bx) / 2
                blobItem[1] += (y - by) / 2
                blobItem[2] += (w - bw) / 2
                blobItem[3] += (h - bh) / 2
                if blobItem[5] < 100:
                    blobItem[5] += 1
        if not found:
            blobs.append([x, y, w, h, id, 0])
        
        
        # mx, my = pygame.mouse.get_pos()
        # glow_img.set_alpha(255)
        # screen.blit(glow_img, (x, y))
    
    temp_blobs = []
    for blobItem in blobs:
        found = False
        to_be_copied = True
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            if id == blobItem[4]:
                found = True
        if not found:
            blobItem[5] -= 1
            if blobItem[5] < 0:
                to_be_copied = False
        if to_be_copied:
            temp_blobs.append(blobItem)
    blobs.clear()
    blobs = temp_blobs.copy()
    temp_blobs.clear()

    for blobItem in blobs:
        bx, by, bw, bh, bid, bf = blobItem
        # print(blobItem)
        glow_img.set_alpha(bf * 3)
        screen.blit(glow_img, (bx, by))

    cv2.imshow("roi", roi)
    # cv2.imshow("Frame", frame)
    # cv2.imshow("Mask", mask)
    # cv2.imshow("output", bg_img)

    
    

    pygame.display.flip()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


pygame.quit()

cap1.release()
cap2.release()
cv2.destroyAllWindows()

