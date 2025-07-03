import cv2
import serial
import time
import numpy as np

ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 115200)

time.sleep(0.5)

cam = cv2.VideoCapture(0)

value_on = [0x7F, 0x00, 0x64, 0x00, 0x00, 0x02]
value_on5 = [0x7F, 0x00, 0x64, 0x00, 0x01, 0x02]
value_on2 = [0x7F, 0x00, 0x50, 0x00, 0x00, 0x02]
value_on6 = [0x7F, 0x00, 0x50, 0x00, 0x01, 0x02]
value_on3 = [0x7F, 0x00, 0x35, 0x00, 0x00, 0x01]
value_on4 = [0x7F, 0x00, 0x30, 0x00, 0x01, 0x02]

value_right_move = [0x7F, 0x40, 0x00, 0x00, 0x01, 0x02]
value_left_move = [0x7F, 0xD0, 0x00, 0x00, 0x01, 0x02]

value_backward = [0x7F, 0x00, 0xC0, 0x00, 0x01, 0x02]

value_right = [0x7F, 0x00, 0x50, 0xF9, 0x00, 0x02]
value_right_close = [0x7F, 0x00, 0x50, 0xF9, 0x01, 0x02]
value_right2 = [0x7F, 0x00, 0x35, 0xF9, 0x00, 0x01]
value_right3 = [0x7F, 0x00, 0x30, 0xF9, 0x01, 0x02]
value_left = [0x7F, 0x00, 0x50, 0x07, 0x00, 0x02]
value_left_close = [0x7F, 0x00, 0x50, 0x07, 0x01, 0x02]
value_left2 = [0x7F, 0x00, 0x35, 0x07, 0x00, 0x01]
value_left3 = [0x7F, 0x00, 0x30, 0x07, 0x01, 0x02]
value_off = [0x7F, 0x00, 0x00, 0x00, 0x00, 0x02]
value_off2 = [0x7F, 0x00, 0x00, 0x00, 0x01, 0x02]

value_rotateleft = [0x7F, 0x00, 0x00, 0x40, 0x00, 0x02]
value_rotateleft3 = [0x7F, 0x00, 0x00, 0x30, 0x01, 0x02]
value_rotate_right = [0x7F, 0x00, 0x00, 0xB0, 0x00, 0x02]
value_rotate_right2 = [0x7F, 0x00, 0x00, 0xB0, 0x01, 0x02]
value_rotate_right3 = [0x7F, 0x00, 0x00, 0xD0, 0x01, 0x02]

value_closeclip = [0x7F, 0x00, 0x00, 0x00, 0x01, 0x01]
value_openclip = [0x7F, 0x00, 0x00, 0x00, 0x00, 0x02]
value_close_up = [0x7F, 0x00, 0x00, 0x00, 0x01, 0x00]

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

stage = 18

stage22_1 = 0
count_green = 0

count = 0

cx = 0
cy = 0
Area = 0

y_lower = np.uint8([20, 140, 110])
y_upper = np.uint8([70, 255, 255])

b_lower = np.uint8([100, 100, 65])
b_upper = np.uint8([255, 255, 255])

g_lower = np.uint8([50, 40, 50])
g_upper = np.uint8([80, 255, 255])

black_lower = np.uint8([0, 0, 0])
black_upper = np.uint8([255, 255, 40])

black_lower2 = np.uint8([0, 0, 0])
black_upper2 = np.uint8([255, 255, 50])

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
            
    elif stage == 4:
        if direction != 5:
            ser.write(serial.to_bytes(value_on))
            time.sleep(0.01)
            print("on")
            direction = 5
        
        time_start = time.perf_counter()
                
        while time.perf_counter() - time_start < 1:
            _, img = cam.read()
            ser.write(serial.to_bytes(value_rotateleft))
            
        ser.write(serial.to_bytes(value_off))
        print("off")
        direction = 0
            
        stage = 5
        
    elif stage == 5:
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
                
                stage = 6
        else:
            count += 1
            ser.write(serial.to_bytes(value_off))
            
    elif stage == 6:
        time_start = time.perf_counter()
        
        if direction != 1:
            ser.write(serial.to_bytes(value_on))
            time.sleep(0.01)
            direction = 1
                
        while time.perf_counter() - time_start < 0.4:
            _, img = cam.read()
            ser.write(serial.to_bytes(value_on2))      
            
        ser.write(serial.to_bytes(value_off))
        print("off")
        direction = 0    
        
        time_start = time.perf_counter()
        
        while time.perf_counter() - time_start < 6:
            _, img = cam.read() 
            
        stage = 7
        
    elif stage == 7:
        if direction != 5:
            ser.write(serial.to_bytes(value_on))
            time.sleep(0.01)
            print("on")
            direction = 5
        
        time_start = time.perf_counter()
                
        while time.perf_counter() - time_start < 1.25:
            _, img = cam.read()
            ser.write(serial.to_bytes(value_rotateleft))
            
        ser.write(serial.to_bytes(value_off))
        print("off")
        direction = 0
            
        stage = 8
        
    elif stage == 8:
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
                
                stage = 9
        else:
            count += 1
            ser.write(serial.to_bytes(value_off))
            
    elif stage == 9:
        if direction != 5:
            ser.write(serial.to_bytes(value_on))
            time.sleep(0.01)
            print("on")
            direction = 5
        
        time_start = time.perf_counter()
                
        while time.perf_counter() - time_start < 1:
            _, img = cam.read()
            ser.write(serial.to_bytes(value_rotateleft))
            
        ser.write(serial.to_bytes(value_off))
        print("off")
        direction = 0
            
        stage = 10
        
    elif stage == 10:
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
                
                stage = 12
        else:
            count += 1
            ser.write(serial.to_bytes(value_off))
            
    elif stage == 12:
        if direction != 6:
            ser.write(serial.to_bytes(value_on))
            time.sleep(0.01)
            print("on")
            direction = 6
        
        time_start = time.perf_counter()
                
        while time.perf_counter() - time_start < 0.75:
            _, img = cam.read()
            ser.write(serial.to_bytes(value_rotate_right))
            
        ser.write(serial.to_bytes(value_off))
        print("off")
        direction = 0
            
        stage = 13
        
    elif stage == 13:
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
                
                stage = 14
        else:
            count += 1
            ser.write(serial.to_bytes(value_off))
            
    elif stage == 14:
        if direction != 6:
            ser.write(serial.to_bytes(value_on))
            time.sleep(0.01)
            print("on")
            direction = 6
        
        time_start = time.perf_counter()
                
        while time.perf_counter() - time_start < 0.25:
            _, img = cam.read()
            ser.write(serial.to_bytes(value_rotate_right))
            
        ser.write(serial.to_bytes(value_off))
        print("off")
        direction = 0
            
        stage = 15
        
    elif stage == 15:
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
                
                stage = 16
        else:
            count += 1
            ser.write(serial.to_bytes(value_off))
            
    elif stage == 16:
        time_start = time.perf_counter()
        
        if direction != 1:
            ser.write(serial.to_bytes(value_on))
            time.sleep(0.01)
            direction = 1
                
        while time.perf_counter() - time_start < 0.4:
            _, img = cam.read()
            ser.write(serial.to_bytes(value_on2))      
            
        ser.write(serial.to_bytes(value_off))
        print("off")
        direction = 0    
        
        time_start = time.perf_counter()
        
        while time.perf_counter() - time_start < 6:
            _, img = cam.read() 
            
        stage = 17

    elif stage == 17:
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
                
                stage = 18

        else:
            ser.write(serial.to_bytes(value_off))
            count += 1

    elif stage == 18:
        detect_line(b_lower, b_upper)

        if count >= 5:

            if cx >= 300 and cx <= 340:
                if direction != 1:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    direction = 1

                print("on2")
                ser.write(serial.to_bytes(value_on3))

            elif cx > 340:
                if direction != 4:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    direction = 4
                    
                print("left")
                ser.write(serial.to_bytes(value_left2))

            elif cx < 300 and cx >0:
                if direction != 3:
                    ser.write(serial.to_bytes(value_on))
                    time.sleep(0.01)
                    print("on")
                    direction = 3
                print("right")
                ser.write(serial.to_bytes(value_right2))

            else:
                ser.write(serial.to_bytes(value_off))
                print("off")
                direction = 0

            if cy > 390:
                ser.write(serial.to_bytes(value_off))
                print("off")
                direction = 0

                time_start = time.perf_counter()

                while time.perf_counter() - time_start < 1:
                    _, img = cam.read()
                    ser.write(serial.to_bytes(value_closeclip))

                time_start = time.perf_counter()

                while time.perf_counter() - time_start < 1:
                    _, img = cam.read()
                    ser.write(serial.to_bytes(value_close_up))

                stage = 19

        else:
            count += 1

    elif stage == 19:
        if direction != 7:
            ser.write(serial.to_bytes(value_on5))
            time.sleep(0.01)
            print("on")
            direction = 7

        time_start = time.perf_counter()

        while time.perf_counter() - time_start < 2:
            _, img = cam.read()
            ser.write(serial.to_bytes(value_backward))

        ser.write(serial.to_bytes(value_off2))
        print("off")
        direction = 0

        stage = 20

    elif stage == 20:
        if direction != 6:
            ser.write(serial.to_bytes(value_on5))
            time.sleep(0.01)
            print("on")
            direction = 6
        
        time_start = time.perf_counter()
                
        while time.perf_counter() - time_start < 0.75:
            _, img = cam.read()
            ser.write(serial.to_bytes(value_rotate_right2))
            
        ser.write(serial.to_bytes(value_off2))
        print("off")
        direction = 0
            
        stage = 21

        time_start = time.perf_counter()

    elif stage == 21:

        img = img[0:480, 150:500]

        detect_line(y_lower, y_upper) 
        
        if count >= 5:

            if cx >= 120 and cx <= 240:
                if direction != 1:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    direction = 1

                print("on2")
                ser.write(serial.to_bytes(value_on6))

            elif cx > 240:
                if direction != 4:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    direction = 4
                    
                print("left")
                ser.write(serial.to_bytes(value_left_close))

            elif cx < 120 and cx >0:
                if direction != 3:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    print("on")
                    direction = 3
                print("right")
                ser.write(serial.to_bytes(value_right_close))

            if time.perf_counter() - time_start >= 2.75:

                ser.write(serial.to_bytes(value_off2))
                print("off")
                direction = 0

                count = 0
                
                stage = 22
            else:
                print("error")

        else:
            ser.write(serial.to_bytes(value_off2))
            count += 1

    elif stage == 22:
        img = img[0:480, 240:360]

        detect_line(g_lower, g_upper)

        if count >= 5:
            print(count_green)

            if stage22_1 == 0:
                if cx == 0 and cy == 0:
                    if direction != 8:
                        ser.write(serial.to_bytes(value_on5))
                        time.sleep(0.01)
                        print("onr")
                        direction = 8
                        
                    print("right")
                    ser.write(serial.to_bytes(value_right_move))

                else:
                    count_green += 1
                    stage22_1 = 1

            if count_green >= 1 or count_green <= 2:

                if cx != 0:
                    if direction != 8:
                        ser.write(serial.to_bytes(value_on5))
                        time.sleep(0.01)
                        print("onr")
                        direction = 8
                            
                    print("right")
                    ser.write(serial.to_bytes(value_right_move))

                else:
                    stage22_1 = 0
        else:
            count += 1
                


        if count_green >= 3:
            stage = 23

    elif stage == 23:
        detect_line(g_lower, g_upper)

        if count >= 5:
            if cx >= 320 and cx <= 380:
                ser.write(serial.to_bytes(value_off2))
                print("off")
                direction = 0

                stage = 24

            elif cx > 380:
                if direction != 8:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    print("onr")
                    direction = 8
                    
                print("right")
                ser.write(serial.to_bytes(value_right_move))

            elif cx < 320 and cx >0:

                if direction != 9:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    print("onl")
                    direction = 9

                print("left")
                ser.write(serial.to_bytes(value_left_move))

            else:
                if direction != 8:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    print("none")
                    direction = 8
                    
                print("right")
                ser.write(serial.to_bytes(value_right_move))

        else:
            count += 1

    elif stage == 24:
        detect_line(g_lower, g_upper)

        if count >= 5:
            
            if cx >= 320 and cx <= 360:
                if direction != 1:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    direction = 1

                print("onf")
                ser.write(serial.to_bytes(value_on4))

            elif cx > 360:
                if direction != 4:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    print("onl")
                    direction = 4
                    
                print("left")
                ser.write(serial.to_bytes(value_left3))

            elif cx < 320 and cx >0:
                if direction != 3:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    print("onr")
                    direction = 3
                print("right")
                ser.write(serial.to_bytes(value_right3))

            else:
                ser.write(serial.to_bytes(value_off2))
                print("off")
                direction = 0

            if cy >= 390:
                ser.write(serial.to_bytes(value_off2))
                print("off")
                direction = 0

                # time_start = time.perf_counter()

                # while time.perf_counter() - time_start < 1:
                #     _, img = cam.read()
                #     ser.write(serial.to_bytes(value_close_up))

                stage = 25

        else:
            count += 1


    elif stage == 25:
        detect_line(g_lower, g_upper)

        if count >= 5:

            if cx >= 300 and cx <= 360:
                time_start = time.perf_counter()

                while time.perf_counter() - time_start < 1:
                    _, img = cam.read()
                    ser.write(serial.to_bytes(value_closeclip))
                
                time_start = time.perf_counter()

                while time.perf_counter() - time_start < 1:
                    _, img = cam.read()
                    ser.write(serial.to_bytes(value_openclip))

                # time_start = time.perf_counter()

                # while time.perf_counter() - time_start < 1:
                #     _, img = cam.read()
                #     ser.write(serial.to_bytes(value_openclip))

                stage = 26

            elif cx > 360:
                if direction != 4:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    print("onl")
                    direction = 4
                    
                print("left")
                ser.write(serial.to_bytes(value_rotateleft3))

            elif cx < 300 and cx >0:
                if direction != 3:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    print("onr")
                    direction = 3
                print("right")
                ser.write(serial.to_bytes(value_rotate_right3))

            else:
                if direction != 3:
                    ser.write(serial.to_bytes(value_on5))
                    time.sleep(0.01)
                    print("onr")
                    direction = 3
                print("right")
                ser.write(serial.to_bytes(value_rotate_right3))

        else:
            count += 1



    # elif stage == 19:
    #     if direction != 6:
    #         ser.write(serial.to_bytes(value_on5))
    #         time.sleep(0.01)
    #         print("on")
    #         direction = 6
        
    #     time_start = time.perf_counter()
                
    #     while time.perf_counter() - time_start < 0.7:
    #         _, img = cam.read()
    #         ser.write(serial.to_bytes(value_rotate_right2))
            
    #     ser.write(serial.to_bytes(value_off2))
    #     print("off")
    #     direction = 0
            
    #     stage = 20

    # elif stage == 20:

    #     detect_line(g_lower, g_upper) 
        
    #     if count >= 5:
    #         if cx == 0 or cy == 0:
    #             if direction != 1:
    #                 ser.write(serial.to_bytes(value_on5))
    #                 time.sleep(0.01)
    #                 direction = 1

    #             print("on2")
    #             ser.write(serial.to_bytes(value_on6))
    
    #         else:   
    #             # time_start = time.perf_counter()

    #             # while time.perf_counter() - time_start < 1:
    #             #     _, img = cam.read()
    #             #     ser.write(serial.to_bytes(value_on4))

    #             ser.write(serial.to_bytes(value_off2))
    #             print("off")
    #             direction = 0

    #             count = 0
                
    #             stage = 21

    #     else:
    #         ser.write(serial.to_bytes(value_off2))
    #         count += 1

    # elif stage == 21:
    #     detect_line(g_lower, g_upper)

    #     if count >= 5:

    #         if cx >= 320 and cx <= 360:
    #             if direction != 1:
    #                 ser.write(serial.to_bytes(value_on5))
    #                 time.sleep(0.01)
    #                 direction = 1

    #             print("onf")
    #             ser.write(serial.to_bytes(value_on4))

    #         elif cx > 360:
    #             if direction != 4:
    #                 ser.write(serial.to_bytes(value_on5))
    #                 time.sleep(0.01)
    #                 print("onl")
    #                 direction = 4
                    
    #             print("left")
    #             ser.write(serial.to_bytes(value_left3))

    #         elif cx < 320 and cx >0:
    #             if direction != 3:
    #                 ser.write(serial.to_bytes(value_on5))
    #                 time.sleep(0.01)
    #                 print("onr")
    #                 direction = 3
    #             print("right")
    #             ser.write(serial.to_bytes(value_right3))

    #         else:
    #             ser.write(serial.to_bytes(value_off2))
    #             print("off")
    #             direction = 0

    #         if cy >= 395:
    #             ser.write(serial.to_bytes(value_off2))
    #             print("off")
    #             direction = 0

    #             # time_start = time.perf_counter()

    #             # while time.perf_counter() - time_start < 1:
    #             #     _, img = cam.read()
    #             #     ser.write(serial.to_bytes(value_close_up))

    #             stage = 22

    #     else:
    #         count += 1

    # elif stage == 22:
    #     detect_line(g_lower, g_upper)

    #     if count >= 5:

    #         if cx >= 320 and cx <= 360:
    #             time_start = time.perf_counter()

    #             while time.perf_counter() - time_start < 1:
    #                 _, img = cam.read()
    #                 ser.write(serial.to_bytes(value_closeclip))
                
    #             time_start = time.perf_counter()

    #             while time.perf_counter() - time_start < 1:
    #                 _, img = cam.read()
    #                 ser.write(serial.to_bytes(value_openclip))

    #             # time_start = time.perf_counter()

    #             # while time.perf_counter() - time_start < 1:
    #             #     _, img = cam.read()
    #             #     ser.write(serial.to_bytes(value_openclip))

    #             stage = 23

    #         elif cx > 360:
    #             if direction != 4:
    #                 ser.write(serial.to_bytes(value_on5))
    #                 time.sleep(0.01)
    #                 print("onl")
    #                 direction = 4
                    
    #             print("left")
    #             ser.write(serial.to_bytes(value_rotateleft3))

    #         elif cx < 320 and cx >0:
    #             if direction != 3:
    #                 ser.write(serial.to_bytes(value_on5))
    #                 time.sleep(0.01)
    #                 print("onr")
    #                 direction = 3
    #             print("right")
    #             ser.write(serial.to_bytes(value_rotate_right3))

    #         else:
    #             ser.write(serial.to_bytes(value_off2))
    #             print("off")
    #             direction = 0

    #     else:
    #         count += 1

        
                
            
    print(stage)

    cv2.imshow("img", img)

    if cv2.waitKey(1) == ord("q"):
        ser.write(serial.to_bytes(value_off))
        break
    
    time.sleep(0.01)

ser.write(serial.to_bytes(value_off))
cam.release()