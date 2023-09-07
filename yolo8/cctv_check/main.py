import threading
import queue
import datetime
from cctv_objectdetect import cctv_objectdetect

result = None
paying = 0
recent_paying = 0
paying_threshold = 5
iou_threshold = 0.4
payment_event = threading.Event()
# 결과를 result 큐에서 수집하는 함수
def collect_results(result_queue):
    # 키오스크 박스에서 일정 시간 이상 머무름 -> 계산했다고 판단 -> 시작시간,끝시간 체크
    # -> db 상의 시간과 대소비교, -> 범위 내에 없을 시, 혹은 데이터 없을 시 도난 의심
    # -> 범위 내에 있을 시 결제 판단 -> 카운팅 로직(countobject) 로 넘겨서 확인
    global result , payment
    start_time = None
    end_time = None
    #payment = None

    ###################################### 시간 감지 부분 #########################################
    while True:
        try:
            iou,result,paying = result_queue.get()
            if result :

                if start_time is None :
                    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #print('start_time',start_time)

            else :
                print( iou,result,paying)


            if iou == 0 and recent_paying > paying_threshold and paying == 0:
                if end_time is None:
                    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #print('end', end_time)

            if iou > iou_threshold:
                recent_paying = paying
    ######################################################################################
            ##################### 도난 여부 판단 부분 #########################
            if start_time is not None and end_time is not None :
                print(start_time,end_time)
                db_time = '2023-09-06 06:24:30' # db에서 받아올 데이터
                if start_time < db_time < end_time :
                    print('payment_completed')
                    payment = True
                    print(payment)
                    payment_event.set()
                else :
                    print('도난 의심상황 발생')
                start_time = None
                end_time = None

        except queue.Empty:
            print("새로운 결과가 아직 없습니다...")
        #time.sleep(1)  # 무한 루프를 피하기 위해 잠시 대기

# current_time을 current_time 큐에서 수집하는 함수
def objectcount(count_queue):
    while True:
        try:
            object_name , number = count_queue.get()
            payment_event.wait()
            global payment
            if payment:
                if object_name == # db 물건종류 데이터 :
                    if number <= # db 물건갯수 데이터 :
                        print(object_name, number) # db 와 물건 종류, 갯수를 비교할 db 데이터를 불러올 곳
                        print('정상 결제되었습니다')
                    else :
                        print('도난')
                else :
                    print('도난')
        except queue.Empty:
            print("아직 새로운 현재 시간이 없습니다...")
        #time.sleep(1)  # 무한 루프를 피하기 위해 잠시 대기

# 결과를 생성하고 result 변수를 업데이트하는 함수


if __name__ == "__main__":
    result_queue = queue.Queue()
    count_queue = queue.Queue()

    detect_thread = threading.Thread(target=cctv_objectdetect, args=(result_queue, count_queue))
    collect_result_thread = threading.Thread(target=collect_results, args=(result_queue,))
    count_thread = threading.Thread(target=objectcount, args=(count_queue,))


    detect_thread.start()
    collect_result_thread.start()
    count_thread.start()

    detect_thread.join()
    collect_result_thread.join()
    count_thread.join()


