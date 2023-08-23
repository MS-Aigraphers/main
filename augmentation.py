# 기본적인 Augmentation은 YOLO ultralytics에서 제공됩니다.
# 해당 코드는 별도의 Augmentation이 더 필요하다고 가정할 때 label 정보도 이미지와 함께 움직여주는 기능을 수행합니다.

import cv2
import os
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage

# YOLO 형식의 bbox 정보를 읽고 쓰기 위한 함수들

def read_yolo_label(label_path):
    with open(label_path, 'r') as f:
        lines = f.readlines()

    bbox_list = []
    for line in lines:
        class_idx, x_center, y_center, width, height = map(float, line.strip().split())
        bbox = {
            'class_idx': int(class_idx),
            'x_center': x_center,
            'y_center': y_center,
            'width': width,
            'height': height
        }
        bbox_list.append(bbox)

    return bbox_list

def write_yolo_label(label_path, bbox_list):
    with open(label_path, 'w') as f:
        for bbox in bbox_list:
            line = f"{bbox['class_idx']} {bbox['x_center']} {bbox['y_center']} {bbox['width']} {bbox['height']}\n"
            f.write(line)


# YOLO 형식의 bbox 정보를 imgaug의 BoundingBox로 변환하는 함수
def yolo_bbox_to_imgaug(yolo_bbox, image_shape):
    x_center, y_center, width, height = yolo_bbox['x_center'], yolo_bbox['y_center'], yolo_bbox['width'], yolo_bbox['height']
    x1 = max((x_center - width / 2) * image_shape[1], 0)
    y1 = max((y_center - height / 2) * image_shape[0], 0)
    x2 = min((x_center + width / 2) * image_shape[1], image_shape[1])
    y2 = min((y_center + height / 2) * image_shape[0], image_shape[0])
    return BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2, label=yolo_bbox['class_idx'])

# imgaug 증강을 위한 시퀀스 생성
augmentation_seq = iaa.Sequential([
    iaa.Fliplr(0.5),  # 50% 확률로 좌우 반전
    iaa.Affine(rotate=(-30, 30)),  # -30에서 30도 사이에서 회전
])

# 입력 이미지와 라벨 디렉토리 설정
# 이 부분은 디렉토리 경로를 맞게 설정해주시면 됩니다.
image_dir = 
aug_image_dir =     #augmentation 이미지 저장할 폴더
label_dir = 
aug_label_dir =     #augmentation 라벨 저장할 폴더

# 이미지와 라벨 파일 목록 가져오기
image_files = os.listdir(image_dir)
label_files = os.listdir(label_dir)

# 각 이미지에 대해 증강 적용
for image_file in image_files:
    if image_file.endswith('.png'):
        image_path = os.path.join(image_dir, image_file)
        label_file = os.path.splitext(image_file)[0] + '.txt'
        label_path = os.path.join(label_dir, label_file)
        aug_label_path = os.path.join(aug_label_dir, label_file)

        # 이미지 로드
        image = cv2.imread(image_path)
        image_height, image_width, _ = image.shape

        # YOLO 형식 라벨 파일 읽기
        bbox_list = read_yolo_label(label_path)

        # imgaug를 사용하여 이미지와 bbox 증강
        bbox_list_aug = [yolo_bbox_to_imgaug(bbox, (image_width, image_height)) for bbox in bbox_list]
        bbs_aug = BoundingBoxesOnImage(bbox_list_aug, shape=image.shape)
        image_aug, bbs_aug = augmentation_seq(image=image, bounding_boxes=bbs_aug)

        # 변경된 bbox 정보를 라벨 파일에 저장
        bbox_list_aug = [{'class_idx': bbox.label, 'x_center': bbox.x1, 'y_center': bbox.y1, 'width': bbox.x2 - bbox.x1, 'height': bbox.y2 - bbox.y1} for bbox in bbs_aug]
        write_yolo_label(aug_label_path, bbox_list_aug)

        # 변경된 이미지를 저장
        cv2.imwrite(os.path.join(aug_image_dir, f"{image_file}"), image_aug)
