def calculate_iou(box1, box2):
    # box1: (x1, y1, x2, y2) format for top-left and bottom-right coordinates
    x1_1, y1_1, x2_1, y2_1 = box1
    x1_2, y1_2, x2_2, y2_2 = box2

    # Calculate the coordinates of the intersection rectangle
    x_intersection = max(0, min(x2_1, x2_2) - max(x1_1, x1_2))
    y_intersection = max(0, min(y2_1, y2_2) - max(y1_1, y1_2))

    # Calculate the area of intersection
    intersection_area = x_intersection * y_intersection

    # Calculate the area of both boxes
    area_box1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area_box2 = (x2_2 - x1_2) * (y2_2 - y1_2)

    # Calculate the Union area
    union_area = area_box1 + area_box2 - intersection_area

    # Calculate IOU
    iou = intersection_area / union_area if union_area != 0 else 0.0

    return iou

