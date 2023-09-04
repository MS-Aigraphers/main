
import math

def check_distance_between_objects(person_bboxes, object_bboxes, min_distance, duration_frames):
    close_for_duration = False
    close_count = 0

    for p_bbox in person_bboxes:
        p_x1, p_y1, p_x2, p_y2 = p_bbox
        p_center_x, p_center_y = (p_x1 + p_x2) // 2, (p_y1 + p_y2) // 2

        for o_bbox in object_bboxes:
            o_x1, o_y1, o_x2, o_y2 = o_bbox
            o_center_x, o_center_y = (o_x1 + o_x2) // 2, (o_y1 + o_y2) // 2

            # Calculate distance between centers
            distance = math.sqrt((p_center_x - o_center_x)**2 + (p_center_y - o_center_y)**2)

            if distance < min_distance:
                close_count += 1
                
    if close_count >= duration_frames:
        close_for_duration = True

    return close_for_duration
