import time
import cv2




def kioskzoneenter(frame, iou, fps, width,paying_threshold,iou_threshold):

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


def countobject(x,y,count_coords,class_name,object_counts_frame,object_detected) :

    if count_coords[0][0] < x < count_coords[2][0] and count_coords[0][1] < y < count_coords[2][1]:

        if class_name == "1 : Ice_cream":
            object_counts_frame['Ice_cream'] = object_counts_frame.get('Ice_cream', 0) + 1
            return True
        
        elif class_name == "2 : Snack":
            object_counts_frame['Snack'] = object_counts_frame.get('Snack', 0) + 1
            return True
        
        elif class_name == "3 : Drink":
            object_counts_frame['Drink'] = object_counts_frame.get('Drink', 0) + 1
            return True
        
        elif class_name == "4 : Ramen":
            object_counts_frame['Ramen'] = object_counts_frame.get('Ramen', 0) + 1
            return True
        
    return False






