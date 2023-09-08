from web.kakao import *      # web에 있는 kakao.py에서 모든 함수를 가져옴
from web.manage import *     # web에 있는 manage.py에서 모든 함수를 가져옴
from eventlogic import *
from django.http import JsonResponse

from datetime import datetime
from requests import request
from django.utils import timezone
from datetime import datetime
import threading
import time

# 1. def kiosk_enter_zone() : 은 모델에서 처리해서 값 보내기로


# 2.   def PaymentTryCheck()  결제시도체크 로직
# 2-a : def KioskZoneEnter() 에서 true 및 CrossLineCheck()에서 out을 반환하면 def PaymentTryCheck() 시작
# 2-b : 키오스크 DB로 쿼리문 실행 로직 시작
# 2-c : 쿼리문으로 키오스크의 결제시간(time) 빼오기
# 2-d : 빼온 time값이 1-b time과 CrossLineCheck()에서 out을 반환한 시간사이의 결제시도 비교하여  (가상의 테이블)
# 2-e : 로그가 있으면 True 반환 및 def PaymentTryCheck() 종료
# 2-f : 로그가 없으면 alert 실행 및 def PaymentTryCheck() 종료

# TODO 모델단에서 어떤식으로 데이터를 던질지 같이 생각해봐야함
def payment_try_check(iou50_10:datetime, payment_time_fromDB:datetime, exit_time:datetime) -> bool:
    # 2-d 결제시도시간과 결제시간 비교
    if iou50_10 < payment_time_fromDB < exit_time:
        print(" OOOO  결제시도 로그가 있습니다.")
        result = True
    else:
        print(" XXXX 결제시도 로그가 없습니다.")
        kakao_alert(time=datetime.datetime.now(), txt="결제시도가 없습니다.")
        result = False

    return result


# 3. def CountObjectFromDB()  사물개수비교
# 3-a : def PaymentTryCheck() 에서 True 반환시 def CountObjectFromDB() 시작
# 3-b : CountObject()의 savecount 숫자가져오기
# 3-c : 키오스크 DB로 쿼리문 실행으로 키오스크의 사물개수 빼오기
# 3-d : 빼온 사물개수와 3-b의 savecount 비교하여 같거나 많으면 True 반환 및 def CountObjectFromDB() 종료
# 3-e : 빼온 사물개수와 3-b의 savecount 비교하여 적으면 alert 실행 및 def CountObjectFromDB() 종료
# TODO 객체탐지 모델과 DB 동시에 불러와야함 / input으로 받을것인가? 파라미터를 그냥 불러올것인가?
def count_object_from_DB(obj_cnt:int, obj_cnt_fromDB:int) -> bool:
    # obj_cnt = kiosk_views.소지한물건갯수_메소드  # 소지하고 있는 물건의 갯수
    # obj_cnt_fromDB = kiosk_views.바코드물건갯수_메소드  # 바코드에 찍힌 물건의 갯수
    # DB views.py에서 obj_cnt_fromDB를 가져오는 방법은 ?
    if obj_cnt >= obj_cnt_fromDB:
        print(" OOOO  카운트가 정상 범위입니다.")
        result = True
    else:
        print(" XXXX  카운트가 비정상 범위입니다.")
        result = False
        kakao_alert(time=datetime.datetime.now(), txt="카운트에 문제가 있습니다.")


    return result

# 생각해봐야할 문제
# 사람 카운팅 할것인가?
# 로직의 시작시간과 끝시간에 대한 분명한 기준을 세워야하는가?
# 여러명일때 정상적으로 체킹이 가능한가?
# 예외적인 부분은 어떤것들이 있을까?

def kakao_alert(time, txt) :
    print(f'{time} {txt}')
    # 0831 작업 중
    # 백단에서 승훈 카톡api랑 연결중 0901 백단에서 코드 수정 중
    pass