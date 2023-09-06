import cv2
import numpy as np
from ultralytics import YOLO
import find_weapon
from calculate_iou import calculate_iou
from kiosk import kioskzoneenter
from kiosk import countobject
from collections import Counter
import datetime

########################## <영상 추출 부분> #################################

cap = cv2.VideoCapture("./cctv_videodata/2023-08-24-15-44-00.mp4")
model_detect = YOLO('./08291455.pt')
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

########################################################################

##################################### <변수 부분> ########################################

kiosk_coords = [(600, 400), (1100, 400), (1100, 800), (600, 800)]  # 키오스크 박스 좌표
kiosk_bbox = (
    kiosk_coords[0][0], kiosk_coords[0][1], kiosk_coords[2][0], kiosk_coords[2][1])  # IOU 계산을 위해 변환 (X,Y,X2,Y2 형태)
count_coords = [(800, 300), (1300, 300), (1300, 800), (800, 800)]  # 카운팅 용 박스

start_time = None
paying_threshold = 5 # 계산 시간 설정부분

object_detected = False
paying = 0
recent_paying = 0
iou_threshold = 0.4
object_keys = []
object_values = []
object_types = []

########################################################################################

########################################## < Main Loop > #################################

while True:
    ret, frame = cap.read()
    if not ret:
        break

    object_counts_list = [] # 객체 카운팅 리스트
    object_counts_frame = {} # 프레임 당 카운팅 정보 저장 리스트

    ###################### 모델 설정 부분 ##############################

    results_detect = model_detect(frame)
    result_detect = results_detect[0]
    bboxes_detect = np.array(result_detect.boxes.xyxy.cpu(), dtype="int")
    classes_detect = np.array(result_detect.boxes.cls.cpu(), dtype="int")

    ##################################################################

    ########################### 객체 탐지 및 키오스크 존 관련 루프 ####################

    for i, (cls, bbox) in enumerate(zip(classes_detect, bboxes_detect)):
        (x, y, x2, y2) = bbox
        class_name = class_names[cls]
        confidence = result_detect.boxes.conf[i]

        ########################## < 각 개체들의 confidence 값 조절 부분, 높을 수록 잘 안잡힘 >################

        if class_name == "6: Weapon" and confidence < 0.7:
            continue
        elif class_name == "0 : Human" and confidence < 0.3:
            continue
        elif confidence < 0.5:
            continue

        ###############################################################################################

        ###################################### < 무기 판단 경고 로직 부분 > ################################

        if class_name == "6 : Weapon":
            cv2.putText(
                frame, "Weapon!!!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
            )  # Weapon 의 confidence 값이 0.7 이상일 경우 출력 프레임에 경고 표시,

        ################################################################################################

        ##################################### < 키오스크 존 입장 여부 및 계산 여부 판단 로직 부분 > #####################

        if class_name == "0 : Human":
            person_bbox = (x, y, x2, y2)
            iou = calculate_iou(kiosk_bbox, person_bbox)
            iou_text = f'IOU: {iou:.2f}'
            cv2.putText(frame, iou_text, (width - 200, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            # 사람일 경우 미리 설정된 kiosk_bbox 와의 iou 계산 및 출력 프레임에 표시

            result, paying = kioskzoneenter(frame, iou, fps, width, paying_threshold,iou_threshold)
            if result:
                cv2.putText(frame,"Okay",(width - 400, 120),cv2.FONT_HERSHEY_PLAIN,2,(0, 0, 255),2)
                # kioskzoneenter 의 result 결괏값이 true 인 경우 (paying 시간이 설정 시간보다 큰 경우) 프레임에 표시

        if paying > paying_threshold:
            object_detected = countobject(x, y, count_coords, class_name, object_counts_frame, object_detected)
            # paying 시간이 설정 시간보다 큰 경우 객체의 숫자를 카운팅 하는 부분

        cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
        cv2.putText(frame,f'{class_name} ({confidence:.2f})',(x, y - 5),cv2.FONT_HERSHEY_PLAIN,2,(0, 0, 225),2,)
        # 객체 인식 결과 (객체 종류 , confidence 값) 을 bbox 와 함께 frame 에 표시하는 부분

        ##############################################################################################################

    #################################### < 인식된 객체에 대하여 갯수를 세는 로직 부분 > #######################################

    if object_detected:
        object_counts_list.append(object_counts_frame)
        object_detected = False

        object_counts_frame = object_counts_list[0]  # 딕셔너리인 것으로 가정

        # 키와 값이 들어 있는 목록 생성
        object_keys = list(object_counts_frame.keys())
        object_values = list(object_counts_frame.values())

        for i in range(len(object_keys)):
            key = object_keys[i]
            value = object_values[i]
        object_types.append([key,value])

        #print(object_types) # ex (drink,3)

    ############################# 객체 카운팅 이후 갯수 판단 로직 부분 #################################

    if iou == 0 and recent_paying > paying_threshold and paying == 0:
        # 값을 추출
        values = [item[1] for item in object_types]

        # Counter를 사용하여 각 값의 발생 횟수를 계산
        value_counts = Counter(values)

        # 백분율 계산
        total_values = len(values)
        percentage_counts = {value: count / total_values * 100 for value, count in value_counts.items()}
        # 백분율 계산 이후  1. 가장 큰 값이 20% 이상 차지할 경우 그 값을 객체의 갯수라고 판단
        #                2. 20% 이하일 경우 모든 프레임에서 가장 많이 인식된 객체의 수를 객체의 갯수라고 판단

        ############################# 갯수 판단 이후 txt 로 저장하는 부분 #################################
        for value, count in value_counts.items():
            #print(f"{value} 값은 {count}번 발생하며, 전체 중 {percentage_counts[value]:.2f}%를 차지합니다.")
            if value == max(values) :

                ###################### txt 이름에 현재시간 추가 ##########################################

                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"output_{timestamp}.txt"  # 파일 이름에 타임스탬프를 사용합니다.

                ####################################################################################


                if percentage_counts[value] > 20 :
                    print(object_types[0][0],max(values),percentage_counts[value])
                    with open(filename, "w") as text_file:
                        text_file.write(f'{object_types[0][0]},{max(values)},{percentage_counts[value]}')
                # 1. 가장 큰 값이 20% 이상 차지할 경우 그 값을 객체의 갯수라고 판단

                else :
                    # 가장 높은 백분율을 가진 객체 클래스 찾기
                    max_percentage_object_class = max(percentage_counts, key=percentage_counts.get)
                    max_percentage_count = value_counts[max_percentage_object_class]
                    print(object_types[0][0],max_percentage_object_class,percentage_counts[max_percentage_object_class])
                    with open(filename, "w") as text_file:
                        text_file.write(f'{object_types[0][0]},{max_percentage_object_class},{percentage_counts[max_percentage_object_class]}')
                # 2. 20% 이하일 경우 모든 프레임에서 가장 많이 인식된 객체의 수를 객체의 갯수라고 판단

                # # 프레임을 이미지로 저장
                # image_filename = f"frame_{timestamp}.jpg"
                # cv2.imwrite(image_filename, frame)

                object_types = []
                object_counts_list = []
                object_counts_frame = []
                object_types = []

        ################################################################################################

    if iou > iou_threshold :
        recent_paying = paying
    cv2.imshow('Frame', frame)
    output.write(frame)

    key = cv2.waitKey(1)
    if key == 27:
        output.write(frame)
        break


cap.release()
output.release()
cv2.destroyAllWindows()
