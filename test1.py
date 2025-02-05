import cv2
import numpy as np

cam =cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cam.read()

    frame = cv2.Canny(frame, 100, 300)

    cv2.imshow('cam', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

12345
