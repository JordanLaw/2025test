import serial
import time

ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 115200)

time.sleep(0.5)

state = False

value_on = [0x7F, 0x00, 0x64, 0x00, 0x00, 0x02]

value_on2 = [0x7F, 0x00, 0x50, 0x00, 0x00, 0x02]

value_off = [0x7F, 0x00, 0x00, 0x00, 0x01, 0x00]

while True:
    print("off")

    ser.write(serial.to_bytes(value_off))

    time.sleep(0.1)

    # print("on")

    # if state == False:

    #     ser.write(serial.to_bytes(value_on))

    #     time.sleep(0.01)

    #     state = True

    # ser.write(serial.to_bytes(value_on2))

    # time.sleep(1)

    