from picamera.array import PiRGBArray
import picamera
from picamera import PiCamera
import time
import cv2

def CaptureImage(camera, rawCapture):
    print('Capturing frames...')
    print('Press Ctrl-C to end')

    try:
        # capture frames from the camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array
            cv2.imwrite('driving_frames/'+str(time.time()) + '.jpg', image)

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

    except (KeyboardInterrupt, picamera.exc.PiCameraValueError):
        print('Stopped')
        pass

if __name__ == "__main__":
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 320)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(640, 320))
    # Set ISO to the desired value
    camera.iso = 800
    # Wait for the automatic gain control to settle
    time.sleep(2)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g

    # allow the camera to warmup
    time.sleep(0.1)

    CaptureImage(camera, rawCapture)
