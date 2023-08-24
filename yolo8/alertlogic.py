import threading
import time

## 객체 탐지기 클래스
import requests
import time

# Define your API credentials or access token
api_key = "YOUR_API_KEY"

# Set the URL for KakaoTalk API
api_url = "https://api.kakaotalk.com/v1/messages/send"

# Initialize a timer variable
start_time = None

# Main loop for object detection
while True:
    if object_detected():  # Replace with your object detection logic
        if start_time is None:
            start_time = time.time()  # Start the timer
        else:
            elapsed_time = time.time() - start_time
            if elapsed_time > 5:
                # Perform actions when object is detected for more than 5 seconds
                message = "Object detected for more than 5 seconds!"
                payload = {
                    "receiver_uuids": ["RECEIVER_UUID"],  # Replace with receiver's UUID
                    "message": message,
                }
                headers = {
                    "Authorization": f"Bearer {api_key}",
                }
                response = requests.post(api_url, json=payload, headers=headers)
                print("Message sent:", response.status_code)
                # Reset the timer
                start_time = None
    else:
        start_time = None  # Reset the timer if no object is detected
    time.sleep(1)  # Adjust the interval as needed

# 7초 후에 객체 감지 중단
time.sleep(7)
detector.stop_detection()