import threading
import time

# 첫 번째 작업을 수행하는 함수
def job1():
    while True:
        print("작업 1 실행 중...")
        time.sleep(5)  # 5초 동안 대기

# 두 번째 작업을 수행하는 함수
def job2():
    while True:
        print("작업 2 실행 중...")
        time.sleep(3)  # 3초 동안 대기

# 스레드 생성 및 실행
thread1 = threading.Thread(target=job1)
thread2 = threading.Thread(target=job2)

thread1.start()
thread2.start()

# 메인 스레드는 종료되지 않고 계속 실행됩니다.
while True:
    pass
