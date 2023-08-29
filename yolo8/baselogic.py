import requests
import threading
import time
from web.kakao import *      # web에 있는 kakao.py에서 모든 함수를 가져옴
from web.manage import *     # web에 있는 manage.py에서 모든 함수를 가져옴
from yolo8.alertlogic import *  # yolo8에 있는 alertlogic.py에서 모든 함수를 가져옴



# def crosslinecheck() :  라인설정
# 객체가 탐지가 일어나면 시작
# a : 사람 아래 box가 가상의 선을 a -> b 순서로 지나가면(a를 먼저터치) in 반환
# b : 사람 아래 box가 가상의 선을 b -> a 순서로 지나가면(b를 먼저터치) out 반환
# 사람 윗박스 좌표 및 아래박스 좌표로 해서 가상의 선에 윗박스 찍고 아래박스 찍으면 out 으로 생각할 수도 있음
# 객체가 탐지가 일어나면 시작
def crosslinecheck(return_value) :

    return "out"



# def objectmovecheck() :   사람과 물건이 함께 움직이는지
# a : 사람 box와 물건 box의 거리가 x거리 이내인지 확인 (거리는 정해야함)
# b : 사람 box와 물건 box의 거리가 x거리 이내이면서 y초간 지속되었으면 True 반환
def objectmovecheck() :
    pass


# def countobject() :
# a : def KioskZoneEnter() true일 경우 상품의 box 카운트값 x에 저장
# b : x초 단위로 savecount변수에 최대카운트값 저장
# c : CrossLineCheck() out 반환하면 로직 종료
def countobject() :
    pass

# def alert()  알림
def alert() :
    pass



# Main Condition

# 1-a : ObjectMoveCheck() true 반환시 키오스크존 진입 로직 시작
if objectmovecheck() == True :
    kioskzoneenter()

# 2-a : def KioskZoneEnter() 에서 true 및 CrossLineCheck()에서 out을 반환하면 def PaymentTryCheck() 시작
if kioskzoneenter() == True and crosslinecheck() == "out" :
    paymenttrycheck()

# 3-a : def PaymentTryCheck() 에서 True 반환시 def countobjectfromDB() 시작
if paymenttrycheck() == True :
    countobjectfromDB()
