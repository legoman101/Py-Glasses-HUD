import cv2
import logging as log

log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()