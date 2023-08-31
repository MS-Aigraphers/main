import time
import cv2

def kioskzoneenter(frame, iou, fps, width,paying_threshold):
    iou_threshold = 0.4
    time_threshold = 20.0


    if iou >= iou_threshold:
        if 'start_time' not in kioskzoneenter.__dict__ or kioskzoneenter.start_time is None:
            kioskzoneenter.start_time = time.time()

        elapsed_time = time.time() - kioskzoneenter.start_time
        elapsed_seconds = int(elapsed_time * fps)

        if elapsed_seconds >= time_threshold:
            paying = int(elapsed_seconds / 15)

            cv2.putText(frame, f'Paying ... {paying} seconds', (width - 400, 80),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            if paying > paying_threshold:
                return True, paying
            return False , paying
    elif iou == 0:
        kioskzoneenter.start_time = None

    return False, 0



