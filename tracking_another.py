import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict

model = YOLO('./runs/detect/train24/weights/best.pt')

video_path = './01.mp4'

cap = cv2.VideoCapture(video_path)

track_history = defaultdict(lambda: [])

while cap.isOpened():

    success, frame = cap.read()

    if success:
        results = model.track(frame, persist=True, conf=0.5)
        print(results[0].boxes)

        boxes = []
        track_ids = []

        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.cpu().tolist()

        annotated_frame = results[0].plot()

        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            track = track_history[track_id]

            track.append((float(x), float(y)))

            if len(track) > 30:
                track.pop()

            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(100, 150, 130), thickness=5)

        cv2.imshow('yolov8 tracking...', annotated_frame)

        key = cv2.waitKey(1)
        if key & 0xff == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()


