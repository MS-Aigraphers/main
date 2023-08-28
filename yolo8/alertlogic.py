import requests
import threading
import time



# def CrossLineCheck()   라인설정
# 객체가 탐지가 일어나면 시작
# a : 사람 아래 box가 가상의 선을 a -> b 순서로 지나가면(a를 먼저터치) in 반환
# b : 사람 아래 box가 가상의 선을 b -> a 순서로 지나가면(b를 먼저터치) out 반환
# 사람 윗박스 좌표 및 아래박스 좌표로 해서 가상의 선에 윗박스 찍고 아래박스 찍으면 out 으로 생각할 수도 있음
# 객체가 탐지가 일어나면 시작

# def ObjectMoveCheck()   사람과 물건이 함께 움직이는지
# a : 사람 box와 물건 box의 거리가 x거리 이내인지 확인 (거리는 정해야함)
# b : 사람 box와 물건 box의 거리가 x거리 이내이면서 y초간 지속되었으면 True 반환

# def CountObject()
# a : def KioskZoneEnter() true일 경우 상품의 box 카운트값 x에 저장
# b : x초 단위로 savecount변수에 최대카운트값 저장
# c : CrossLineCheck() out 반환하면 로직 종료


# 1.  def KioskZoneEnter()  키오스크존 진입 로직  (1번 카메라에 사람과 물건을 인식한다)
# 1-a : ObjectMoveCheck() true 반환시 키오스크존 진입 로직 시작
# 1-b : 키오스크로 존에 IOU가 80프로 이상 겹치면 time 로그 찍고 start.time() 시작
# 1-c : 키오스크에 10초이상 있으면 키오스크 return True 및
# 1-d : start.time() 실행 없이 CrossLineCheck()에서 out 반환시 alert 실행 후 진입 로직 종료

# 2.   def PaymentTryCheck()  결제시도체크 로직
# 2-a : def KioskZoneEnter() 에서 true 및 CrossLineCheck()에서 out을 반환하면 def PaymentTryCheck() 시작
# 2-b : 키오스크 DB로 쿼리문 실행 로직 시작
# 2-c : 쿼리문으로 키오스크의 결제시간(time) 빼오기
# 2-d : 빼온 time값이 1-b time과 CrossLineCheck()에서 out을 반환한 시간사이의 결제시도 비교하여  (가상의 테이블)
# 2-e : 로그가 있으면 True 반환 및 def PaymentTryCheck() 종료
# 2-f : 로그가 없으면 alert 실행 및 def PaymentTryCheck() 종료

# 3. def CountObjectFromDB()  사물개수비교
# 3-a : def PaymentTryCheck() 에서 True 반환시 def CountObjectFromDB() 시작
# 3-b : CountObject()의 savecount 숫자가져오기
# 3-c : 키오스크 DB로 쿼리문 실행으로 키오스크의 사물개수 빼오기
# 3-d : 빼온 사물개수와 3-b의 savecount 비교하여 같거나 많으면 True 반환 및 def CountObjectFromDB() 종료
# 3-e : 빼온 사물개수와 3-b의 savecount 비교하여 적으면 alert 실행 및 def CountObjectFromDB() 종료

# 생각해봐야할 문제
# 사람 카운팅 할것인가?
# 로직의 시작시간과 끝시간에 대한 분명한 기준을 세워야하는가?
# 여러명일때 정상적으로 체킹이 가능한가?
# 예외적인 부분은 어떤것들이 있을까?






## 객체 탐지기 클래스

import time

# Define your API credentials or access token
api_key = "YOUR_API_KEY"

# Set the URL for KakaoTalk API
api_url = "https://api.kakaotalk.com/v1/messages/send"

# Initialize a timer variable
start_time = None

# Main loop for object detection
# while True:
#     if object_detected():  # Replace with your object detection logic
#         if start_time is None:
#             start_time = time.time()  # Start the timer
#         else:
#             elapsed_time = time.time() - start_time
#             if elapsed_time > 5:
#                 # Perform actions when object is detected for more than 5 seconds
#                 message = "Object detected for more than 5 seconds!"
#                 payload = {
#                     "receiver_uuids": ["RECEIVER_UUID"],  # Replace with receiver's UUID
#                     "message": message,
#                 }
#                 headers = {
#                     "Authorization": f"Bearer {api_key}",
#                 }
#                 response = requests.post(api_url, json=payload, headers=headers)
#                 print("Message sent:", response.status_code)
#                 # Reset the timer
#                 start_time = None
#     else:
#         start_time = None  # Reset the timer if no object is detected
#     time.sleep(1)  # Adjust the interval as needed
#
# # 7초 후에 객체 감지 중단
# time.sleep(7)
# detector.stop_detection()