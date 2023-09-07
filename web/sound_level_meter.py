import sounddevice as sd
import numpy as np
from datetime import datetime

class SoundMonitor:
    def __init__(self, duration=10):
        self.duration = duration

    def print_sound(self, indata, outdata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        if int(volume_norm) > 80:
            now = datetime.today()
            print(f'{now.year}.{now.month}.{now.day} {now.hour}:{now.minute}:{now.second} 소음이 감지 되었습니다.')

    def start_monitoring(self):
        with sd.Stream(callback=self.print_sound):
            sd.sleep(self.duration * 1000)

if __name__ == "__main__":
    monitor = SoundMonitor(duration=10)
    monitor.start_monitoring()






# import sounddevice as sd
# from numpy import linalg as LA
# import numpy as np
# import time
# from datetime import datetime


# datetime.today()            # 현재 날짜 가져오기
# datetime.today().year        # 현재 연도 가져오기
# datetime.today().month      # 현재 월 가져오기
# datetime.today().day        # 현재 일 가져오기
# datetime.today().hour        # 현재 시간 가져오기
# datetime.today().minute      # 현재 분 가져오기
# datetime.today().second 

# duration = 10  # seconds

# while True:
#     present_wave=[]
#     compare_wave=[]

#     def print_sound(indata, outdata, frames, time, status):
#         volume_norm = np.linalg.norm(indata)*10
#         # print (int(volume_norm))
#         if (int(volume_norm)) > 80:
#             print(f'{datetime.today().year}.{datetime.today().month}.{datetime.today().day} {datetime.today().hour}:{datetime.today().minute}:{datetime.today().second} 소음이 감지 되었습니다.')
#     with sd.Stream(callback=print_sound):
#         sd.sleep(duration * 1000)




# class SoundMonitor:
#     def __init__(self, duration=3):
#         self.duration = duration

#     def print_sound(self, indata, outdata, frames, time, status):
#         volume_norm = np.linalg.norm(indata) * 10
#         if int(volume_norm) > 80:
#             timestamp = datetime.today().strftime('%Y.%m.%d %H:%M:%S')
#             message=print(f'{timestamp} 소음이 감지 되었습니다.')
#         return message

#     def start_monitoring(self):
#         with sd.Stream(callback=self.print_sound):
#             sd.sleep(self.duration * 1000)


# if __name__ == "__main__":
#     duration = 3  # 원하는 녹음 시간 (초)
#     monitor = SoundMonitor(duration)
#     monitor.start_monitoring()