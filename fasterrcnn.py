import os
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.rpn import AnchorGenerator
from torch.utils.data import DataLoader
from torchvision.transforms import functional as F
import albumentations as A
from albumentations.pytorch import ToTensorV2
from tqdm import tqdm
import numpy as np


class YOLOLabelTransform:
    def __init__(self, num_classes, img_size):
        self.num_classes = num_classes
        self.img_size = img_size

    def __call__(self, targets):
        transformed_targets = []

        for target in targets:
            class_id, x_center, y_center, width, height = target
            class_id = int(class_id)

            x_min = (x_center - width / 2) * self.img_size[0]
            y_min = (y_center - height / 2) * self.img_size[1]
            x_max = (x_center + width / 2) * self.img_size[0]
            y_max = (y_center + height / 2) * self.img_size[1]

            bbox = [x_min, y_min, x_max, y_max]

            transformed_targets.append({
                'boxes': torch.tensor([bbox], dtype=torch.float32),
                'labels': torch.tensor([class_id], dtype=torch.int64)
            })

        return transformed_targets  # 리스트로 래핑하지 않음




class CustomDataset(Dataset):
    def __init__(self, image_dir, label_dir, num_classes, img_size):
        self.image_dir = image_dir
        self.label_dir = label_dir
        self.img_size = img_size
        self.label_transform = YOLOLabelTransform(num_classes, img_size)

        # 이미지와 라벨 파일이 모두 존재하는 경우만 포함
        self.image_names = [name for name in os.listdir(self.image_dir) if self._has_label(name)]

    def _has_label(self, image_name):
        label_name = os.path.splitext(image_name)[0] + '.txt'
        label_path = os.path.join(self.label_dir, label_name)
        return os.path.exists(label_path)

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, idx):
        image_name = self.image_names[idx]
        image_path = os.path.join(self.image_dir, image_name)
        label_name = os.path.splitext(image_name)[0] + '.txt'
        label_path = os.path.join(self.label_dir, label_name)

        image = Image.open(image_path).convert('RGB')

        transform = A.Compose([
            A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            A.GaussianBlur(blur_limit=3),
            A.MotionBlur(blur_limit=5),
            A.HorizontalFlip(),
            ToTensorV2(),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        augmented = transform(image=np.array(image))
        image = augmented['image']

        with open(label_path, 'r') as f:
            labels = f.readlines()

        targets = [[float(x) for x in label.strip().split(' ')] for label in labels]
        transformed_targets = self.label_transform(targets)

        return image, transformed_targets



# 사용 예시
image_dir = 'ultralytics/cfg/cctv2nd_dataset/train/images'
label_dir = 'ultralytics/cfg/cctv2nd_dataset/train/labels'
num_classes = 7  # 클래스 개수에 맞게 수정
img_size = (640, 640)  # 이미지 크기에 맞게 수정

dataset = CustomDataset(image_dir, label_dir, num_classes, img_size)
def collate_fn(batch):
    images, targets_list = zip(*batch)
    transformed_targets_list = []

    for targets in targets_list:
        if targets:
            transformed_targets = {
                'boxes': torch.stack([target['boxes'][0] for target in targets]),
                'labels': torch.stack([target['labels'][0] for target in targets])
            }
            transformed_targets_list.append(transformed_targets)

    # 빈 타겟을 가진 배치를 필터링합니다.
    filtered_indices = [i for i, targets in enumerate(transformed_targets_list) if targets['boxes'].shape[0] > 0]
    images = [images[i] for i in filtered_indices]
    transformed_targets_list = [transformed_targets_list[i] for i in filtered_indices]

    return images, transformed_targets_list






dataloader = DataLoader(dataset, batch_size=64, shuffle=True, collate_fn=collate_fn)



# Load a pre-trained Faster R-CNN model
def get_model(num_classes):
    # Load a pre-trained ResNet-50 model
    backbone = torchvision.models.detection.backbone_utils.resnet_fpn_backbone('resnet50', pretrained=True)

    # Define the number of anchor boxes and their sizes
    rpn_anchor_generator = AnchorGenerator(
        sizes=((32, 64, 128, 256, 512),),
        aspect_ratios=((0.5, 1.0, 2.0),) * 5
    )

    # Create the Faster R-CNN model
    model = FasterRCNN(
        backbone,
        num_classes=num_classes,
        rpn_anchor_generator=rpn_anchor_generator
    )

    return model


# Initialize the model
model = get_model(num_classes)

# Define your optimizer and learning rate scheduler
optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.0005)
lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=10, T_mult=2, eta_min=1e-6)

best_mAP = 0.0
best_model_path = 'best_faster_rcnn_model.pth'

# 모델 훈련
num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    epoch_losses = []

    for images, targets_list in tqdm(dataloader, desc=f"Epoch [{epoch + 1}/{num_epochs}]"):
        images = [F.to_tensor(img) for img in images]

        targets = targets_list

        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values())

        optimizer.zero_grad()
        losses.backward()
        optimizer.step()

        epoch_losses.append(losses.item())

    mean_loss = sum(epoch_losses) / len(epoch_losses)
    print(f"Epoch [{epoch + 1}/{num_epochs}] - Mean Loss: {mean_loss:.4f}")

    # 검증 세트에서 모델 평가
    model.eval()
    with torch.no_grad():
        # ... 검증 세트에서 추론을 수행하고 mAP를 계산합니다.
        # 실제 mAP 계산 코드로 아래 줄을 대체하세요.
        val_mAP = 0.5

    if val_mAP > best_mAP:
        best_mAP = val_mAP
        # 최적 모델의 파라미터 저장
        torch.save(model.state_dict(), best_model_path)
        print(f"Best model saved with mAP: {best_mAP}")
