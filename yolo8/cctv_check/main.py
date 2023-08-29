import cv2
from ultralytics import YOLO
import numpy as np
import os
import find_weapon

count = 0
cap = cv2.VideoCapture("./cctv_videodata/weapon_Sequence.mp4")  # 여기 영상 경로를 넣어주세요
#model_face = YOLO('./yolov8n-face.pt')
model_detect = YOLO('./08291455.pt') # 사용할 모델.pt 를 넣어주세요
#model_detect = YOLO('yolov8s.pt')

find_weapon.show_weapons() # weapon_list를 생성하는 함수


# 동영상 저장을 위한 VideoWriter 객체 생성
fps = cap.get(cv2.CAP_PROP_FPS)  # 원본 동영상의 프레임 속도
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 원본 동영상의 프레임 너비
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 원본 동영상의 프레임 높이
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 동영상 코덱 설정
output = cv2.VideoWriter("output2.mp4", fourcc, fps, (width, height))  # 출력 동영상 파일 설정, 이름도 변경 가능
#print(fps,width,height,fourcc,output)


class_names = []
with open("./classes.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        class_names.append(line.strip())   # class_names 리스트에 classes.txt 파일을 불러와서 저장시킴
#print(class_names)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # results_face = model_face(frame)
    # result_face = results_face[0]
    # bboxes_face = np.array(result_face.boxes.xyxy.cpu(), dtype="int")
    # classes_face = np.array(result_face.boxes.cls.cpu(), dtype="int")

    results_detect = model_detect(frame)
    result_detect = results_detect[0]
    bboxes_detect = np.array(result_detect.boxes.xyxy.cpu(), dtype="int")
    classes_detect = np.array(result_detect.boxes.cls.cpu(), dtype="int")

    # for i, (cls, bbox) in enumerate(zip(classes_face, bboxes_face)):
    #     (x, y, x2, y2) = bbox
    #     class_name = class_names[cls]
        
    #     # 얼굴 영역 추출
    #     face_region = frame[y:y2, x:x2]

    #     # 얼굴 영역을 blur 처리
    #     blurred_face = cv2.GaussianBlur(face_region, (21, 21), 0)

    #     # blur 처리된 영역을 다시 원본 이미지에 적용
    #     frame[y:y2, x:x2] = blurred_face

    #     cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)  # 얼굴 바운딩 박스의 색상을 변경합니다.
    #     cv2.putText(frame, class_name, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        
    for i, (cls, bbox) in enumerate(zip(classes_detect, bboxes_detect)):
        (x, y, x2, y2) = bbox
        class_name = class_names[cls]
        confidence = result_detect.boxes.conf[i]
        if confidence < 0.5 :
            continue
        if class_name == 'Weapon' :
            count += 1
        cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
        cv2.putText(frame, f'{class_name} ({confidence:.2f})', (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 225), 2)
        
        find_weapon.is_weapon(class_name, frame)
        
        # 무기 소지 시의 프레임을 이미지로 저장
    find_weapon.save_weapon('./weapon/')

    cv2.imshow('Frame', frame)
    output.write(frame)

    key = cv2.waitKey(1)
    if key == 27:
        output.write(frame)
        break


cap.release()
output.release()  # 출력 동영상 파일 닫기
cv2.destroyAllWindows()