import cv2, platform

captureStor = cv2.VideoCapture('rtsp://root.pass@169.254.203.231/axis-media/media.amp')

captureLiten = cv2.VideoCapture('rtsp://root.pass@169.254.135.93/axis-media/media.amp')

#gray = cv2.cvtColor(captureStor, cv2.COLOR_BGR2GRAY)
#cv2.imshow('captureStor', gray)
