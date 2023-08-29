import sounddevice as sd
from numpy import linalg as LA
import numpy as np
import time
from datetime import datetime

datetime.today()            # 현재 날짜 가져오기
datetime.today().year        # 현재 연도 가져오기
datetime.today().month      # 현재 월 가져오기
datetime.today().day        # 현재 일 가져오기
datetime.today().hour        # 현재 시간 가져오기
datetime.today().minute      # 현재 분 가져오기
datetime.today().second 

duration = 10  # seconds
while True:
    present_wave=[]
    compare_wave=[]

    def print_sound(indata, outdata, frames, time, status):
        volume_norm = np.linalg.norm(indata)*10
        # print (int(volume_norm))
        if (int(volume_norm)) > 80:
            print(f'{datetime.today().year}.{datetime.today().month}.{datetime.today().day} {datetime.today().hour}:{datetime.today().minute}:{datetime.today().second} 소음이 감지 되었습니다.')

    with sd.Stream(callback=print_sound):
        sd.sleep(duration * 1000)

