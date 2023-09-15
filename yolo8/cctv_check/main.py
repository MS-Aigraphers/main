import threading
import queue
import cv2
from cctv_objectdetect import cctv_objectdetect
from mailsend import *
import os
# from views import *
# from web.home.models import Kiosk  # 장고 모델 불러오기

# 변수를 저장하기 위한 전역 사전 생성
global_vars = {
    "result": None,
    "payment": None,
    "paying": 0,
    "recent_paying": 0,
    "paying_threshold": 5,
    "iou_threshold": 0.4,
    'distance': False,
    'human_inside' : False,
    'start_time' : None,
    'end_time' : None,
    'prev_inside' : False,
    'countobject' : False,
    'weapon' : False,
    'order_number' : 0,

}
payment_event = threading.Event()
cross_event = threading.Event()
move_event = threading.Event()
collect_event = threading.Event()


def weapon_situation(weapon_queue) :
    frame_count = 0
    while True:
        try :
            frame,global_vars['human_inside'] = weapon_queue.get()
            frame_count += 1
            print(global_vars['distance'])
            if global_vars['distance'] :

                print('무기 소지자 발생')

                # countup 무기 소지자
                global_vars['distance'] = False
            else :
                print('무기 발견')

            # Save the frame as an image
            image_filename = os.path.join('./weapon', f"frame_{frame_count}.jpg")
            cv2.imwrite(image_filename, frame)

        except :
            print("새로운 결과가 아직 없습니다...")



def check_crossing_line(cross_queue):
    while True:
        try:

            global_vars['human_inside'] = cross_queue.get()


            if global_vars['human_inside'] :

                cross_event.set()
            elif global_vars['human_inside'] is False :
                global_vars['distance'] = False

        except:
            print("새로운 결과가 아직 없습니다...")


def ObjectMoveCheck(object_queue):
    while True:
        try:
            cross_event.wait()
            print(global_vars['payment'],'payment')

            global_vars['distance'] = object_queue.get()
            if global_vars['distance']:
                global_vars['payment'] = False

                move_event.set()
            elif global_vars['distance']:
                move_event.set()
                global_vars['payment'] = False



            # elif global_vars['distance'] is False :


        except queue.Empty:
            print("새로운 결과가 아직 없습니다...")


def collect_results(result_queue):
    steal_frame = 0
    payment_frame = 0
    while True:
        try:
            iou, result, paying,frame = result_queue.get()
            move_event.wait()

            print(iou, result, paying)
            if result:
                if global_vars["start_time"] is None:
                    # global_vars["start_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    global_vars["start_time"] = 100
                    payment_frame +=1
                    image_filename = os.path.join('./payment', f"frame_{payment_frame}.jpg")
                    cv2.imwrite(image_filename, frame)

                    #print(global_vars["start_time"],'start')


            print(global_vars['human_inside'], 'human')
            print(global_vars['prev_inside'], 'prev')
            if global_vars['prev_inside'] is True and global_vars['human_inside'] is False :
                # global_vars["end_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                global_vars["end_time"] = 150


            if global_vars["start_time"] is not None and global_vars["end_time"] is not None:
                print(global_vars["start_time"], global_vars["end_time"])

                # # Django 모델에서 레코드의 id를 기반으로 payment_time 값을 가져옵니다.
                # kiosk_record = Kiosk.objects.get(id=1)  # 원하는 레코드의 id로 1을 대체하세요.
                # db_time = kiosk_record.payment_time

                db_time = 130  # db에서 받아올 데이터
                if global_vars["start_time"] <db_time and db_time <global_vars["end_time"] :
                    print('결제 완료')
                    global_vars["payment"] = True
                    print(global_vars["payment"])
                    global_vars['countobject'] = True

                    global_vars["start_time"] = None
                    global_vars["end_time"] = None

                    payment_event.set()

                else :
                    print('계산하는 척 도난')
                    send_email(receiver='onekid2@naver.com', content='naver.com', title='미결제')
                    steal_frame += 1
                    # Save the frame as an image
                    image_filename = os.path.join('./steal', f"frame_{steal_frame}.jpg")
                    cv2.imwrite(image_filename, frame)

                    # countup_계산한척##########################################



            if global_vars['prev_inside'] is True and global_vars['human_inside'] is False and global_vars["payment"] is False:
                if global_vars['distance'] :
                    print('도망')
                    send_email(receiver='onekid2@naver.com', content='naver.com', title='미결제')
                    steal_frame += 1
                    # Save the frame as an image
                    image_filename = os.path.join('./steal', f"frame_{steal_frame}.jpg")
                    cv2.imwrite(image_filename, frame)

                    ## countup_튄놈###################################################

                    global_vars["payment"] = None
                else :
                    global_vars["payment"] = None



            global_vars['prev_inside'] = global_vars['human_inside']

                    # if global_vars['prev_inside'] is True and global_vars['human_inside'] is False and global_vars[
                    #     "payment"] is False:
                    #     print('도난')




        except queue.Empty:
            print("새로운 결과가 아직 없습니다...")


def objectcount(count_queue):
    count_frame = 0
    while True:
        try:
            object_name, number = count_queue.get()
            payment_event.wait()
            count_frame +=1
            # kiosk_record = Kiosk.objects.get(store_name='store1')
            # print('갯수',global_vars["payment"])
            if global_vars['countobject']:
                print(object_name,number,'물건')

                # 물건 이름 , 갯수 db 추가 부분##############################################
                # if object_name == kiosk_record.object_label :
                #     if number == kiosk_record.object_count :
                #         print('정상 결제')
                #         global_vars['order_number'] += 1
                #         create_sales_record(global_vars['order_number'],object_name,number,'store1')
                #         # countup 물건 갯수
                #
                #     else :
                #        print('도난')
                #         # countup_개수안맞은놈#####################
                #
                # else :
                #     print('도난')
                #     # countup_개수안맞은놈######################
                #########################################################################



                global_vars['countobject'] = False
        except queue.Empty:
            print("아직 새로운 현재 시간이 없습니다...")


if __name__ == "__main__":
    result_queue = queue.Queue()
    count_queue = queue.Queue()
    object_queue = queue.Queue()
    cross_queue = queue.Queue()
    weapon_queue = queue.Queue()

    detect_thread = threading.Thread(target=cctv_objectdetect,
                                     args=(result_queue, count_queue, object_queue, cross_queue,weapon_queue))
    collect_result_thread = threading.Thread(target=collect_results, args=(result_queue,))
    count_thread = threading.Thread(target=objectcount, args=(count_queue,))
    object_thread = threading.Thread(target=ObjectMoveCheck, args=(object_queue,))
    cross_thread = threading.Thread(target=check_crossing_line, args=(cross_queue,))
    weapon_thread =threading.Thread(target=weapon_situation, args=(weapon_queue,))

    detect_thread.start()
    collect_result_thread.start()
    count_thread.start()
    object_thread.start()
    cross_thread.start()
    weapon_thread.start()

    detect_thread.join()
    collect_result_thread.join()
    count_thread.join()
    object_thread.join()
    cross_thread.join()
    weapon_thread.join()
