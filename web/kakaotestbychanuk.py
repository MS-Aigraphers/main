import requests
import json
import time

def access_keys(file_path):
    keys = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # 빈 칸과 개행 문자 제거
            if line and '=' in line:  # 빈 줄이 아니고, '=' 기호가 있는 경우에만 처리
                key, value = line.split('=')
                keys[value] = key.strip("'")
    return keys

#code url  https://kauth.kakao.com/oauth/authorize?client_id=자신의 rest key값&redirect_uri=https://example.com/oauth&response_type=code
url = 'https://kauth.kakao.com/oauth/token'
FILE_PATH = "./kaokao_key_copy.txt"
rest_api_key, authorize_code = access_keys(FILE_PATH)  # rest_api
redirect_uri = "https://example.com/oauth"

import requests

### Refresh token 발췌
def f_auth():
    data = {
        'grant_type': 'authorization_code',
        'client_id': rest_api_key,
        'redirect_uri': redirect_uri,
        'code': authorize_code,
    }

    response = requests.post(url, data=data)
    tokens = response.json()

    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    r_token = ts["refresh_token"]
    return r_token

### Refresh toekn 을 갖고 new Access token 발행
def f_auth_refresh(r_token):
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    data = {
        "grant_type": "refresh_token",
        "client_id": rest_api_key,
        "refresh_token": r_token
    }
    response = requests.post(url, data=data)
    tokens = response.json()

    with open(r"kakao_code.json", "w") as fp:
        json.dump(tokens, fp)
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    token = ts["access_token"]
    return token

def f_send_talk(token, text):
    header = {'Authorization': 'Bearer ' + token}
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    post = {
        'object_type': 'text',
        'text': text,
        'link': {
            'web_url': 'https://https://developers.kakao.com',
        },
        'button_title': '웹으로 이동',
    }
    data = {'template_object': json.dumps(post)}
    print("f_send_talk 정상작동 ")
    return requests.post(url, headers=header, data=data)

r_token = f_auth()

while True:
    token = f_auth_refresh(r_token)
    f_send_talk (token, '소음이 감지 되었습니다. www.naver.com')
    time.sleep(180)

# from PyKakao import Message
#
#
# def access_keys(path:str):
#     with open(path, 'r') as f:
#         result = f.readlines()
#         result = [word.strip() for word in result]
#     return result
#
#
# def kakao_alert():
#     api = Message(api_key)
#     auth_url = api.get_url_for_generating_code()
#     print(auth_url)
#
# FILE_PATH = "/Users/chris/Desktop/AIgraphers/AIgraphers/web/kaokao_key_copy.txt"
# api_key, authorize_code = access_keys(FILE_PATH)
#
# kakao_alert()














# from PyKakao import Message
#
#
# def access_keys(path:str):
#     with open(path, 'r') as f:
#         result = f.readlines()
#         result = [word.strip() for word in result]
#     return result
#
#
# def kakao_alert():
#     api = Message(api_key)
#     auth_url = api.get_url_for_generating_code()
#     print(auth_url)
#
# FILE_PATH = "/Users/chris/Desktop/AIgraphers/AIgraphers/web/kaokao_key_copy.txt"
# api_key, authorize_code = access_keys(FILE_PATH)
#
# kakao_alert()