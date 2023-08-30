from web.kakao import *      # web에 있는 kakao.py에서 모든 함수를 가져옴
from web.manage import *     # web에 있는 manage.py에서 모든 함수를 가져옴
from baselogic import *
from django.http import JsonResponse

from datetime import datetime
from requests import request
from django.utils import timezone
from datetime import datetime
import threading
import time


# 1.  def KioskZoneEnter()  키오스크존 진입 로직  (1번 카메라에 사람과 물건을 인식한다)
# 1-a : ObjectMoveCheck() true 반환시 키오스크존 진입 로직 시작
# 1-b : 키오스크로 존에 IOU가 80프로 이상 겹치면 time 로그 찍고 start.time() 시작
# 1-c : 키오스크에 10초이상 있으면 키오스크 return True 및
# 1-d : start.time() 실행 없이 crosslinecheck()에서 out 반환시 alert 실행 후 진입 로직 종료

global start_time
start_time = datetime.now()
def kiosk_zone_enter(iou: float):
    result = False
    date_format = '%Y.%m.%d.%H.%M.%S'

    # IOU 80%가 넘는지 확인
    if iou >= 80:
        # 키오스크존에 진입 시간 기록
        start_time = datetime.now()

        while True:
            end_time_str = request.GET.get('IOU_time', None)  # IOU에서 전달되는 값으로 판단하는 것 같습니다.
            if end_time_str is not None:
                end_time = datetime.strptime(end_time_str, date_format)

                # 키오스크에 10초 이상 머무르는지 확인
                if (end_time - start_time).seconds >= 10:
                    result = True
                    break
                else:
                    kakao_alert(txt="키오스크에 10초 이상 머물지 않았습니다.")
                    break  # 10초 미만 머무른 경우에도 반복문 탈출
            else:
                # IOU_time 값이 전달되지 않은 경우에 대한 처리
                # 필요한 로직을 추가해야 합니다.
                pass

            time.sleep(1)
    else:
        raise Exception("IOU 값이 80% 미만입니다.")

    return result


    # 키오스크로 존에 IOU가 80프로 이상 겹치면 time 로그 찍고 start.time() 시작
    # 키오스크에 10초이상 있으면 키오스크 return True 및


# 2.   def PaymentTryCheck()  결제시도체크 로직
# 2-a : def KioskZoneEnter() 에서 true 및 CrossLineCheck()에서 out을 반환하면 def PaymentTryCheck() 시작
# 2-b : 키오스크 DB로 쿼리문 실행 로직 시작
# 2-c : 쿼리문으로 키오스크의 결제시간(time) 빼오기
# 2-d : 빼온 time값이 1-b time과 CrossLineCheck()에서 out을 반환한 시간사이의 결제시도 비교하여  (가상의 테이블)
# 2-e : 로그가 있으면 True 반환 및 def PaymentTryCheck() 종료
# 2-f : 로그가 없으면 alert 실행 및 def PaymentTryCheck() 종료

def paymenttrycheck():
    # 2-b 쿼리날리기
    # 2-c 쿼리결과값 받아오기
    # payment_time_fromDB = 쿼리문을 통해 받은 결제시간
    # 2-d 결제시도시간과 결제시간 비교
    # payment_time
        pass


# DB 값 3개
# 1. 시간(우리가 임의로), 개수,

# f_send_talk(token, text)

# 3. def CountObjectFromDB()  사물개수비교
# 3-a : def PaymentTryCheck() 에서 True 반환시 def CountObjectFromDB() 시작
# 3-b : CountObject()의 savecount 숫자가져오기
# 3-c : 키오스크 DB로 쿼리문 실행으로 키오스크의 사물개수 빼오기
# 3-d : 빼온 사물개수와 3-b의 savecount 비교하여 같거나 많으면 True 반환 및 def CountObjectFromDB() 종료
# 3-e : 빼온 사물개수와 3-b의 savecount 비교하여 적으면 alert 실행 및 def CountObjectFromDB() 종료

def countobjectfromDB() :
    pass

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