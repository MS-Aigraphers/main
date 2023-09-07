import requests
import json
import time
from sound_level_meter import SoundMonitor

#code url  https://kauth.kakao.com/oauth/authorize?client_id=자신의 rest key값&redirect_uri=https://example.com/oauth&response_type=code



class KakaoMessenger:
    def __init__(self, file_path, redirect_uri, message):
        self.file_path = file_path
        self.redirect_uri = redirect_uri
        self.message = message
        self.rest_api_key, self.authorize_code = self.access_keys()

    def access_keys(self):
        keys = {}
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()  # 빈 칸과 개행 문자 제거
                if line and '=' in line:  # 빈 줄이 아니고, '=' 기호가 있는 경우에만 처리
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

        with open("kakao_code01.json", "w") as fp:
            json.dump(tokens, fp)
        with open("kakao_code01.json", "r") as fp:
            ts = json.load(fp)
        r_token = ts["refresh_token"]
        return r_token

    def f_auth_refresh(self, r_token):
        url = 'https://kauth.kakao.com/oauth/token'
        with open("kakao_code01.json", "r") as fp:
            ts = json.load(fp)
        data = {
            "grant_type": "refresh_token",
            "client_id": self.rest_api_key,
            "refresh_token": r_token
        }
        response = requests.post(url, data=data)
        tokens = response.json()

        with open(r"kakao_code01.json", "w") as fp:
            json.dump(tokens, fp)
        with open("kakao_code01.json", "r") as fp:
            ts = json.load(fp)
        token = ts["access_token"]
        return token

    def f_send_talk(self, token):
        url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
        header = {'Authorization': 'Bearer ' + token}
        post = {
            'object_type': 'text',
            'text': self.message,
            'link': {
                'web_url': 'https://https://developers.kakao.com',
            },
            'button_title': '웹으로 이동',
        }
        data = {'template_object': json.dumps(post)}
        return requests.post(url, headers=header, data=data)

    def start_messaging(self):
        r_token = self.f_auth()
        token = self.f_auth_refresh(r_token)
        self.f_send_talk(token)

# 사용 예시
if __name__ == "__main__":
    file_path = "./kaokao_key_copy.txt"
    redirect_uri = 'https://example.com/oauth'
    message = '소음이 감지 되었습니다. \n www.naver.com'
    # duration = 3  # 원하는 녹음 시간 (초)
    
    messenger = KakaoMessenger(file_path, redirect_uri, message)
    # messenger.start_messaging()
    # monitor = SoundMonitor(duration)
    # detect=monitor.start_monitoring()

    r_token = messenger.f_auth()
    token = messenger.f_auth_refresh(r_token)
    messenger.f_send_talk(token)








# def access_keys(file_path):
#     keys = {}
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#         for line in lines:
#             line = line.strip()  # 빈 칸과 개행 문자 제거
#             if line and '=' in line:  # 빈 줄이 아니고, '=' 기호가 있는 경우에만 처리
#                 key, value = line.split('=')
#                 keys[value] = key.strip("'")
#     return keys

# def kakao_message(token, message):
#     url = 'https://kauth.kakao.com/oauth/token'
#     FILE_PATH = "./kaokao_key_copy.txt"
#     rest_api_key, authorize_code = access_keys(FILE_PATH)  # rest_api
#     redirect_uri = 'https://example.com/oauth'

#     def f_auth():
#         data = {
#             'grant_type': 'authorization_code',
#             'client_id': rest_api_key,
#             'redirect_uri': redirect_uri,
#             'code': authorize_code,
#         }

#         response = requests.post(url, data=data)
#         tokens = response.json()

#         with open("kakao_code01.json", "w") as fp:
#             json.dump(tokens, fp)
#         with open("kakao_code01.json", "r") as fp:
#             ts = json.load(fp)
#         r_token = ts["refresh_token"]
#         return r_token

#     def f_auth_refresh(r_token):
#         with open("kakao_code01.json", "r") as fp:
#             ts = json.load(fp)
#         data = {
#             "grant_type": "refresh_token",
#             "client_id": rest_api_key,
#             "refresh_token": r_token
#         }
#         response = requests.post(url, data=data)
#         tokens = response.json()

#         with open(r"kakao_code01.json", "w") as fp:
#             json.dump(tokens, fp)
#         with open("kakao_code01.json", "r") as fp:
#             ts = json.load(fp)
#         token = ts["access_token"]
#         return token

#     def f_send_talk(token, text):
#         header = {'Authorization': 'Bearer ' + token}
#         url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
#         post = {
#             'object_type': 'text',
#             'text': text,
#             'link': {
#                 'web_url': 'https://https://developers.kakao.com',
#             },
#             'button_title': '웹으로 이동',
#         }
#         data = {'template_object': json.dumps(post)}
#         return requests.post(url, headers=header, data=data)

#     r_token = f_auth()

#     while True:
#         token = f_auth_refresh(r_token)
#         f_send_talk (token, message)
#         time.sleep(180)



# file_path='/Users/iamseungman/Aigrapher/main/web/kaokao_key_copy.txt'


# # 메시지 전송
# kakao_message(file_path, '소음이 감지 되었습니다. \n www.naver.com')
