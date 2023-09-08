import math


def check_distance_between_objects(person_bbox, other_bbox,min_distance):
    close_for_duration = False
    close_count = 0

    x1, y1, x2, y2 = person_bbox
    x3, y3, x4, y4 = other_bbox

    # "person" 객체의 중심 좌표 계산
    person_center_x = (x1 + x2) / 2
    person_center_y = (y1 + y2) / 2

    # 다른 객체의 중심 좌표 계산
    other_center_x = (x3 + x4) / 2
    other_center_y = (y3 + y4) / 2

    # "person" 객체와 다른 객체 간의 유클리드 거리 계산
    distance = math.sqrt((person_center_x - other_center_x) ** 2 + (person_center_y - other_center_y) ** 2)

    if distance < min_distance:
        return True

    # if close_count >= duration_frames:
    #     close_for_duration = True

    return False