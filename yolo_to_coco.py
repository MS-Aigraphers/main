import json
import os
import glob
import shutil

# COCO JSON 파일을 읽는 함수
def load_coco_json(json_file_path):
    with open(json_file_path, 'r') as json_file:
        coco_data = json.load(json_file)
    return coco_data

# COCO 형식 데이터를 YOLO 형식으로 변환하는 함수
def coco_to_yolo(annotation, image_width, image_height):
    category_id = annotation['category_id']
    bbox = annotation['bbox']
    x, y, width, height = bbox
    x_center = x + width / 2
    y_center = y + height / 2
    x_center /= image_width
    y_center /= image_height
    width /= image_width
    height /= image_height

    return f"{category_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"

json_paths = glob.glob(os.path.join('./Website_Screenshots_data', '*','*.json'))

for json_path in json_paths:
    # COCO JSON 파일을 로드
    coco_data = load_coco_json(json_path)

    for image_info in coco_data['images']:
        # 이미지 파일 이름 가져오기
        image_file_name = image_info['file_name']
        image_width = image_info['width']
        image_height = image_info['height']

        # 이미지 파일 경로 확인
        source_image_path = os.path.join(os.path.dirname(json_path), image_file_name)
        if not os.path.exists(source_image_path):
            print(f"Image file {image_file_name} not found.")
            continue

        # 이미지 파일 이동
        destination_image_dir = os.path.join(os.path.dirname(json_path), 'images')
        os.makedirs(destination_image_dir, exist_ok=True)  # images 디렉토리 생성
        destination_image_path = os.path.join(destination_image_dir, image_file_name)
        shutil.move(source_image_path, destination_image_path)

        # 해당 이미지에 대한 annotation들 가져오기
        annotations_for_image = [ann for ann in coco_data['annotations'] if ann['image_id'] == image_info['id']]

        # COCO 데이터를 YOLO 데이터로 변환하여 리스트로 저장
        yolo_data_list = [coco_to_yolo(ann, image_width, image_height) for ann in annotations_for_image]

        # YOLO 데이터를 파일로 저장
        yolo_file_name = os.path.splitext(image_file_name)[0] + '.txt'
        yolo_file_dir = os.path.join(os.path.dirname(json_path), 'labels')
        os.makedirs(yolo_file_dir, exist_ok=True)  # labels 디렉토리 생성
        yolo_file_path = os.path.join(yolo_file_dir, yolo_file_name)
        with open(yolo_file_path, 'w') as yolo_file:
            for line in yolo_data_list:
                yolo_file.write(line + '\n')

