import cv2
import serial
import time
import numpy as np

ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 115200)

time.sleep(0.5)

cam = cv2.VideoCapture(0)

'''
Change the value if your robot is too fast or slow
'''
value_on = [0x7F, 0x00, 0x64, 0x00, 0x00, 0x02]
value_on2 = [0x7F, 0x00, 0x50, 0x00, 0x00, 0x02]

value_right = [0x7F, 0x00, 0x50, 0xF9, 0x00, 0x02]
value_left = [0x7F, 0x00, 0x50, 0x07, 0x00, 0x02]

value_off = [0x7F, 0x00, 0x00, 0x00, 0x00, 0x02]

value_rotateleft = [0x7F, 0x00, 0x00, 0x40, 0x00, 0x02]
value_rotate_right = [0x7F, 0x00, 0x00, 0xB0, 0x00, 0x02]

status = False

time_start = 0

'''
stop = 0
forward = 1
backward = 2
rightward = 3
leftward = 4
rotate_right = 5
rotate_left = 6
'''
direction = 0

stage = 1

stage22_1 = 0
count_green = 0

count = 0

cx = 0
cy = 0
Area = 0

'''
find the HSV value for other color by yourself
'''
y_lower = np.uint8([20, 140, 110])
y_upper = np.uint8([70, 255, 255])

def detect_line(lower_array, upper_array):
    global cx, cy , extLeft, extRight, extTop, extBot, img
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_array, upper_array)

    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        Area = cv2.contourArea(c)

        if Area >= 1000:
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

    else:
        cx = 0
        cy = 0

    print(f"cx: {cx} cy: {cy}")
    

while True:

    _, img = cam.read()

    if stage == 1: 
        img = img[400:480, 150:500]

        detect_line(y_lower, y_upper) 
        
        if count >= 5:

            if cx >= 160 and cx <= 200:
                if direction != 1:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    direction = 1

                print("on2")
                ser.write(serial.to_bytes(value_on2))

            elif cx > 200:
                if direction != 4:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    direction = 4
                    
                print("left")
                ser.write(serial.to_bytes(value_left))

            elif cx < 160 and cx >0:
                if direction != 3:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    print("on")
                    direction = 3
                print("right")
                ser.write(serial.to_bytes(value_right))

            else:
                time_start = time.perf_counter()
                
                if direction != 1:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    direction = 1
                
                while time.perf_counter() - time_start < 0.1:
                    _, img = cam.read()
                    ser.write(serial.to_bytes(value_on2))
                    
                ser.write(serial.to_bytes(value_off))
                print("off")
                direction = 0

                count = 0
                
                stage = 2

        else:
            ser.write(serial.to_bytes(value_off))
            count += 1

    elif stage == 2:
        if direction != 6:
            ser.write(serial.to_bytes(value_on))
            time.sleep(0.01)
            print("on")
            direction = 6
        
        time_start = time.perf_counter()
                
        while time.perf_counter() - time_start < 0.5:
            _, img = cam.read()
            ser.write(serial.to_bytes(value_rotate_right))
            
        ser.write(serial.to_bytes(value_off))
        print("off")
        direction = 0
            
        stage = 3
        
    elif stage == 3:
        img = img[400:480, 150:500]

        detect_line(y_lower, y_upper) 
        
        if count > 5:
            if cx >= 160 and cx <= 200:
                if direction != 1:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    direction = 1

                print("on2")
                ser.write(serial.to_bytes(value_on2))

            elif cx > 200:
                if direction != 4:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    direction = 4
                    
                print("left")
                ser.write(serial.to_bytes(value_left))

            elif cx < 160 and cx >0:
                if direction != 3:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    print("on")
                    direction = 3
                print("right")
                ser.write(serial.to_bytes(value_right))

            else:
                time_start = time.perf_counter()
                
                while time.perf_counter() - time_start < 0.1:
                    _, img = cam.read()
                    ser.write(serial.to_bytes(value_on2))
                    
                ser.write(serial.to_bytes(value_off))
                print("off")
                direction = 0
                
                count = 0
                
                stage = 4
        else:
            count += 1
            ser.write(serial.to_bytes(value_off))

'''
Write your code to control your robot and command them in different stage
'''
    elif stage == 4:
        
       
                
            
    print(stage)

    cv2.imshow("img", img)

    if cv2.waitKey(1) == ord("q"):
        ser.write(serial.to_bytes(value_off))
        break
    
    time.sleep(0.01)

ser.write(serial.to_bytes(value_off))
cam.release()
