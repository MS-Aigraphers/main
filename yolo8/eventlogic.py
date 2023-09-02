from web.kakao import *  # web에 있는 kakao.py에서 모든 함수를 가져옴
from web.manage import *  # web에 있는 manage.py에서 모든 함수를 가져옴
from yolo8.alertlogic import *  # yolo8에 있는 alertlogic.py에서 모든 함수를 가져옴
from datetime import datetime
from web.kiosk import views as kiosk_views

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


# TODO 모델에서 만들어질 이벤트 로직 모두 정리하기 <모델단에서 생성됨>
def crossline_check(return_value, time): #
    # 라인두개 만들어서  바깥쪽 A / 안쪽 B
    # B-> A 이면 out 리턴과 동시에 시간반환
    # A-> B in 리턴
    return "out"



def object_move_check(return_value):
    # def objectmovecheck() :   사람과 물건이 함께 움직이는지
    # a : 사람 box와 물건 box의 거리가 x거리 이내인지 확인 (거리는 정해야함)
    # b : 사람 box와 물건 box의 거리가 x거리 이내이면서 y초간 지속되었으면 True 반환
    pass
def kiosk_enter_zone(return_value) :
    pass
def payment_try_check(return_value) :
    pass
def count_object():
    # a : def KioskZoneEnter() true일 경우 상품의 box 카운트값 x에 저장
    # b : x초 단위로 savecount변수에 최대카운트값 저장
    # c : CrossLineCheck() out 반환하면 로직 종료
    pass



# Main Condition
if __name__ == "__main__":
    # TODO : xxx_메서드 부분은 모델부분과 연결해야합니다 <데이터 변경 필요 부분>.
    # 물건 소지 여부 판단 Logic

    possession_of_item = kiosk_views.물건소지여부_메소드  # 물건 소지 여부 Boolean으로 T/F판단 TODO : 데이터 변경 필요
    if possession_of_item != True:
        raise Exception("키오스크 안들리고 나갑니다.")

    # 키오스크존 n% 10초 유지 여부 판단 Logic
    iou = kiosk_views.IOU값_메소드  # IOU 값 TODO : 데이터 변경 필요 <모델>
    if alertlogic.kiosk_zone_enter(iou) != True and crossline_check() != "out":
        exit_time = datetime.now()
        print(f"이탈 시간 : {exit_time}")
        txt = "키오스크존에서 10초 이상 머물지 않았습니다."
        raise Exception(txt)
        # kakao_alert(time=datetime.datetime.now(), txt=txt)

    # 결제 시도 내역 판단 Logic
    iou50_10 = kiosk_views.IOU_10초유지_메소드  # IOU 50% 10초 이상 유지에 성공한 시각 TODO : 데이터 변경 필요
    payment_time_fromDB = kiosk_views.결제시도_메소드  # 결제시도 시각 TODO : 데이터 변경 필요
    exit_time = kiosk_views.나간시점_메소드  # 나간시각_메소드 TODO : 데이터 변경 필요
    # 3-a : def PaymentTryCheck() 에서 True 반환시 def countobjectfromDB() 시작
    if alertlogic.payment_try_check(iou50_10, payment_time_fromDB, exit_time) != True:
        print(f"이탈 시간 : {exit_time}")
        txt = "결제시도가 없었습니다."
        raise Exception(txt)
        # kakao_alert(time=datetime.datetime.now(), txt=txt")

    # 물건 갯수 판단 Logic
    obj_cnt = kiosk_views.소지한물건갯수_메소드  # 소지하고 있는 물건의 갯수
    obj_cnt_fromDB = kiosk_views.바코드물건갯수_메소드  # 바코드에 찍힌 물건의 갯수
    if alertlogic.count_object_from_DB(obj_cnt, obj_cnt) != True:
        exit_time = datetime.now()
        print(f"이탈 시간 : {exit_time}")
        txt = "물건개수에 문제가 있습니다."
        raise Exception(txt)
        # kakao_alert(time=datetime.datetime.now(), txt=txt")

    print("정상 결제되었습니다. 끝")
