import cv2
import numpy as np
from ultralytics import YOLO
import find_weapon
from calculate_iou import calculate_iou
import time


cap = cv2.VideoCapture("./cctv_videodata/2023-08-24-15-44-00.mp4")
model_detect = YOLO('./08291455.pt')

find_weapon.show_weapons()

######## 추가부분
kiosk_coords = [(600, 400), (1100, 400), (1100, 800), (600, 800)]    #키오스크 박스 좌표
kiosk_bbox = (kiosk_coords[0][0],kiosk_coords[0][1],kiosk_coords[2][0],kiosk_coords[2][1]) # IOU 계산을 위해 변환 (X,Y,X2,Y2 형태)
count_coords = [(800, 300), (1300, 300), (1300, 800), (800, 800)] # 카운팅 용 박스

frames_above_threshold = 0 # 프레임 수를 카운팅하는 변수
start_time = None
##############

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter("output2.mp4", fourcc, fps, (width, height))

class_names = []
with open("./classes.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        class_names.append(line.strip())

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results_detect = model_detect(frame)
    result_detect = results_detect[0]
    bboxes_detect = np.array(result_detect.boxes.xyxy.cpu(), dtype="int")
    classes_detect = np.array(result_detect.boxes.cls.cpu(), dtype="int")

    for i, (cls, bbox) in enumerate(zip(classes_detect, bboxes_detect)):
        (x, y, x2, y2) = bbox
        class_name = class_names[cls]
        confidence = result_detect.boxes.conf[i]

        if class_name == '6: Weapon' and confidence <0.7 :
            continue
        elif class_name == '0 : Human' and confidence <0.3 :
            continue
        elif confidence < 0.5 :
            continue

        if class_name == '0 : Human':
            person_bbox = (x, y, x2, y2)
            iou = calculate_iou(kiosk_bbox,person_bbox)
            iou_text = f'IOU: {iou:.2f}'
            cv2.putText(frame, iou_text, (width - 200, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

            #####추가부분
            iou_threshold = 0.4 # 기준 IOU 값
            time_threshold = 20.0  # 기준 프레임, IOU  값이 0.4 보다 큰 시간이 20보다 커질경우 계산 중이라고 판단


            if iou >= iou_threshold:
                frames_above_threshold += 1
                if start_time is None:
                    start_time = time.time()
                elapsed_time = time.time() - start_time  # 경과 시간을 계산하는 부분

                # Convert frames to seconds
                elapsed_seconds = int(elapsed_time * fps) # GPT 기준 frame에서 시간을 얻는 식, 실제 시간과 달라 추가적으로 작업을 했다
                #print(elapsed_seconds)
                if elapsed_seconds >= time_threshold:
                    paying = int(elapsed_seconds/15) # 15 정도로 나누니까 실제 시간과 비슷해짐
                    cv2.putText(frame, f'Paying ... {paying} seconds',
                                (width - 400, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                    if paying > 10 :
                        cv2.putText(frame, f'Okay',
                                (width - 400, 120), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            elif iou == 0 :
                start_time = None  # iou 값이 0이 될 때 계산 완료라고 판단, 이 경우 Human 이 잠깐 없어지면 계산이 끝났다고 판단하여 실행되어 버린다.


        cv2.polylines(frame, [np.array(kiosk_coords)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.polylines(frame, [np.array(count_coords)], isClosed=True, color=(255, 0, 0), thickness=2)
        # 박스 표시 부분
        ##################################################################
        cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
        cv2.putText(frame, f'{class_name} ({confidence:.2f})', (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 225), 2)

        find_weapon.is_weapon(class_name, frame)

    find_weapon.save_weapon('./weapon/')

    cv2.imshow('Frame', frame)
    output.write(frame)

    key = cv2.waitKey(1)
    if key == 27:
        output.write(frame)
        break

cap.release()
output.release()
cv2.destroyAllWindows()
