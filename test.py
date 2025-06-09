import cv2
import serial
import time
import numpy as np

ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 115200)

time.sleep(0.5)

cam = cv2.VideoCapture(0)

value_on = [0x7F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]

value_off = [0x7F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

lower = np.uint8([0, 0, 0])
upper = np.uint8([255, 255, 70])

while True:

    _, img = cam.read()

    img = img[0:480, 250:390]

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)

    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(f"cx: {cx} cy: {cy}")

            extLeft = tuple(c[c[:, :,0].argmin()][0])
            extRight = tuple(c[c[:, :,0].argmax()][0])
            extTop = tuple(c[c[:, :,1].argmin()][0])
            extBot = tuple(c[c[:, :,1].argmax()][0])

            cv2.drawContours(img, c, -1, (0,255,0), 1)
            cv2.line(img, (cx,0), (cx,480), (255,0,0), 1)
            cv2.line(img, (0,cy), (640,cy), (255,0,0), 1)
            cv2.circle(img, extLeft, 8, (0,0,255), -1)
            cv2.circle(img, extRight, 8, (0,255,0), -1)
            cv2.circle(img, extTop, 8, (255,0,), -1)
            cv2.circle(img, extBot, 8, (255,255,0), -1)

            if cx < 65 or cx > 85:
                ser.write(serial.to_bytes(value_on))

            else:
                ser.write(serial.to_bytes(value_off))


    cv2.imshow("img", img)

    if cv2.waitKey(1) and 0xff == ("q"):
        break