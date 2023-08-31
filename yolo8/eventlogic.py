from web.kakao import *  # web에 있는 kakao.py에서 모든 함수를 가져옴
from web.manage import *  # web에 있는 manage.py에서 모든 함수를 가져옴
from yolo8.alertlogic import *  # yolo8에 있는 alertlogic.py에서 모든 함수를 가져옴
from datetime import datetime

import requests
import threading
import time
import alertlogic


# def crosslinecheck() :  라인설정
# 객체가 탐지가 일어나면 시작
# a : 사람 아래 box가 가상의 선을 a -> b 순서로 지나가면(a를 먼저터치) in 반환
# b : 사람 아래 box가 가상의 선을 b -> a 순서로 지나가면(b를 먼저터치) out 반환
# 사람 윗박스 좌표 및 아래박스 좌표로 해서 가상의 선에 윗박스 찍고 아래박스 찍으면 out 으로 생각할 수도 있음
# 객체가 탐지가 일어나면 시작
# 쉽게 말해서 나가는 사람 탐지하는 로직
def crossline_check(return_value):
    return "out"


# def objectmovecheck() :   사람과 물건이 함께 움직이는지
# a : 사람 box와 물건 box의 거리가 x거리 이내인지 확인 (거리는 정해야함)
# b : 사람 box와 물건 box의 거리가 x거리 이내이면서 y초간 지속되었으면 True 반환
def object_move_check():
    pass


# def countobject() :
# a : def KioskZoneEnter() true일 경우 상품의 box 카운트값 x에 저장
# b : x초 단위로 savecount변수에 최대카운트값 저장
# c : CrossLineCheck() out 반환하면 로직 종료
def count_object():
    pass




# Main Condition
if __name__ == "__main__":
    # 아래 데이터들은 그냥 임의로 적어둠
    # TODO : 데이터 변경 필요
    iou = 80
    ioux_y = datetime.now()  # IOU x% y초 이상 유지에 성공한 시각
    payment_time_fromDB = datetime.now()  # DB에 있는 결제 시각
    exit_time = datetime.now()  # 가게를 나간 시각

    # 2-a : def KioskZoneEnter() 에서 true 및 CrossLineCheck()에서 out을 반환하면 def PaymentTryCheck() 시작
    if alertlogic.kiosk_zone_enter(iou) != True:
        raise Exception("키오스크존에서 10초 이상 머물지 않았습니다.")

    if crossline_check() != "out":
        raise Exception("crossline_check 함수의 결과값이 `out`이 아닙니다.")

    # 3-a : def PaymentTryCheck() 에서 True 반환시 def countobjectfromDB() 시작
    if alertlogic.payment_try_check() != True:
        raise Exception("물건 개수가 맞지 않습니다.")
