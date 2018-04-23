import sys
import cv2
import time
from multiprocessing import Pool
from upload_video import encode_and_send_frame


camera_index = 0 # 0 is usually the built-in webcam
#capture_rate = 30
rekog_max_labels = 123
rekog_min_conf = 50.0


def video_capture():

    argv_len = len(sys.argv)

    cap = cv2.VideoCapture(0) #Use 0 for built-in camera. Use 1, 2, etc. for attached cameras.
    pool = Pool(processes=3)

    frame_count = 0
    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        #cv2.resize(frame, (640, 360));
        if ret is False:
            break

        #if frame_count % capture_rate == 0:
        pool.apply_async(encode_and_send_frame, (frame, frame_count, True, False, False,)).get()
        time.sleep(2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return


video_capture()