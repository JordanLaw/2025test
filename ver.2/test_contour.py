import cv2
import serial
import time
import numpy as np

ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 115200)

time.sleep(0.5)

cam = cv2.VideoCapture(0)

value_on = [0x7F, 0x00, 0x64, 0x00, 0x00, 0x01]
value_on2 = [0x7F, 0x00, 0x35, 0x00, 0x00, 0x01]

value_right = [0x7F, 0x00, 0x35, 0xF9, 0x00, 0x01]
value_left = [0x7F, 0x00, 0x35, 0x07, 0x00, 0x01]
value_off = [0x7F, 0x00, 0x00, 0x00, 0x00, 0x01]

value_close = [0x7F, 0x00, 0x00, 0x00, 0x01, 0x01]
value_up = [0x7F, 0x00, 0x00, 0x00, 0x01, 0x00]

status = False

'''
stop = 0
forward = 1
backward = 2
rightward = 3
leftward = 4
'''
direction = 0

stage = 1

count = 0

cx = 0
cy = 0

lower = np.uint8([0, 100, 65])
upper = np.uint8([15, 255, 255])

time_start = 0
time_end = 0

while True:

    _, img = cam.read()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)

    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            

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

    else:
        cx = 0
        cy = 0

    print(f"cx: {cx} cy: {cy}")
    
    if stage == 1:  
        if count >= 5:

            if cx >= 300 and cx <= 340:
                if direction != 1:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    direction = 1

                print("on2")
                ser.write(serial.to_bytes(value_on2))

            elif cx > 340:
                if direction != 4:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    direction = 4
                    
                print("left")
                ser.write(serial.to_bytes(value_left))

            elif cx < 300 and cx >0:
                if direction != 3:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    print("on")
                    direction = 3
                print("right")
                ser.write(serial.to_bytes(value_right))

            else:
                ser.write(serial.to_bytes(value_off))
                print("off")
                direction = 0

            if cy >= 425:
                ser.write(serial.to_bytes(value_off))
                print("off")
                direction = 0

                stage = 2

        else:
            count += 1

    if stage == 2:
        time_start = time.perf_counter()
        
        while time.perf_counter() - time_start <= 2:
            ser.write(serial.to_bytes(value_close))

        time_start = time.perf_counter()    

        while time.perf_counter() - time_start <= 2:
            ser.write(serial.to_bytes(value_up))
        
        # ser.write(serial.to_bytes(value_up))

        stage = 3


    cv2.imshow("img", img)

    if cv2.waitKey(1) and 0xff == ("q"):
        ser.write(serial.to_bytes(value_off))
        break

ser.write(serial.to_bytes(value_off))
cam.release()