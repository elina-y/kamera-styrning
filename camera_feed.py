import cv2

captureStor = cv2.VideoCapture('rtsp://root.pass@169.254.203.231/axis-media/media.amp')

captureLiten = cv2.VideoCapture('rtsp://root.pass@169.254.135.93/axis-media/media.amp')

#gray = cv2.cvtColor(captureStor, cv2.COLOR_BGR2GRAY)
#cv2.imshow('captureStor', gray)

import cv2, platform
#import numpy as np

#cam = "mms://194.90.203.111/cam2"
#cam = 0 # Use  local webcam.

cap = cv2.VideoCapture(captureStor)
if not cap:
    print("!!! Failed VideoCapture: invalid parameter!")

while(True):
    # Capture frame-by-frame
    ret, current_frame = cap.read()
    if type(current_frame) == type(None):
        print("!!! Couldn't read frame!")
        break

    # Display the resulting frame
    cv2.imshow('frame',current_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the capture
cap.release()
cv2.destroyAllWindows()
