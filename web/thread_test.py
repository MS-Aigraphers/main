import threading
import time
import requests
import json
import sounddevice as sd
import numpy as np
from datetime import datetime
#https://kauth.kakao.com/oauth/authorize?client_id=자신의 rest key값&redirect_uri=https://example.com/oauth&response_type=code

class KakaoMessenger:
    def __init__(self, file_path, redirect_uri):
        self.file_path = file_path
        self.redirect_uri = redirect_uri
        self.rest_api_key, self.authorize_code = self.access_keys()
        self.access_token = None
        self.refresh_token = None
        self.sound_detected = threading.Event()

    def access_keys(self):
        keys = {}
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=')
                    keys[value] = key.strip("'")
        return keys

    def f_auth(self):
        url = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.rest_api_key,
            'redirect_uri': self.redirect_uri,
            'code': self.authorize_code,
        }

        response = requests.post(url, data=data)
        tokens = response.json()

        with open("kakao_code.json", "w") as fp:
            json.dump(tokens, fp)

        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]

    def f_auth_refresh(self):
        url = 'https://kauth.kakao.com/oauth/token'
        data = {
            "grant_type": "refresh_token",
            "client_id": self.rest_api_key,
            "refresh_token": self.refresh_token
        }

        response = requests.post(url, data=data)
        tokens = response.json()

        with open("kakao_code.json", "w") as fp:
            json.dump(tokens, fp)

        self.access_token = tokens["access_token"]

    def f_send_talk(self, text):
        header = {'Authorization': 'Bearer ' + self.access_token}
        url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
        post = {
            'object_type': 'text',
            'text': text,
            'link': {
                'web_url': 'https://developers.kakao.com',
            },
            'button_title': '웹으로 이동',
        }
        data = {'template_object': json.dumps(post)}
        requests.post(url, headers=header, data=data)

    def start_messaging(self, message):
        while True:
            if self.sound_detected.wait(1800):  # 30분 동안 기다림
                self.f_send_talk(message)
                self.sound_detected.clear()  # 이벤트 리셋

class SoundMonitor(threading.Thread):
    def __init__(self, duration=10, messenger=None):
        super().__init__()
        self.duration = duration
        self.messenger = messenger

    def print_sound(self, indata, outdata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        if int(volume_norm) > 80:
            now = datetime.today()
            print(f'{now.year}.{now.month}.{now.day} {now.hour}:{now.minute}:{now.second} 소음이 감지 되었습니다.')
            if self.messenger:
                self.messenger.sound_detected.set()  # 소음 감지 이벤트 설정

    def run(self):
        with sd.Stream(callback=self.print_sound):
            sd.sleep(self.duration * 1000)

if __name__ == "__main__":
    file_path = "./kakao_key_copy.txt"
    redirect_uri = 'https://example.com/oauth'
    message = '소음이 감지 되었습니다. \n www.naver.com'
    
    messenger = KakaoMessenger(file_path, redirect_uri)

    # Start Sound Monitoring in a separate thread
    monitor = SoundMonitor(duration=10, messenger=messenger)
    monitor.start()

    # Start Messaging in the main thread
    messenger.f_auth()
    messenger.start_messaging(message)
