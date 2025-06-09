import cv2
import numpy as np

def nil(self):
    pass

cap =cv2.VideoCapture(0)

cv2.namedWindow('trackBar')
cv2.createTrackbar('HL', 'trackBar', 0, 255, nil)
cv2.createTrackbar('HH', 'trackBar', 0, 255, nil)
cv2.createTrackbar('SL', 'trackBar', 0, 255, nil)
cv2.createTrackbar('SH', 'trackBar', 0, 255, nil)
cv2.createTrackbar('VL', 'trackBar', 0, 255, nil)
cv2.createTrackbar('VH', 'trackBar', 0, 255, nil)

while True:
    _, img = cap.read()

    img = img[0:480, 250:390]

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    HL = cv2.getTrackbarPos('HL', 'trackBar')
    HH = cv2.getTrackbarPos('HH', 'trackBar')
    SL = cv2.getTrackbarPos('SL', 'trackBar')
    SH = cv2.getTrackbarPos('SH', 'trackBar')
    VL = cv2.getTrackbarPos('VL', 'trackBar')
    VH = cv2.getTrackbarPos('VH', 'trackBar')

    low_b = np.uint8([HL, SL, VL])
    high_b = np.uint8([HH, SH, VH])

    mask = cv2.inRange(hsv, low_b, high_b)

    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        Area =cv2.contourArea(c)

        cv2.drawContours(img, c,-1, (0, 255, 0), 1)
        cv2.imshow("image", img)
        cv2.imshow("Mask", mask)

        if cv2.waitKey (1) & 0xff == 27:
            break