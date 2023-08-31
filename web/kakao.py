import requests
import json
import time

#code url  https://kauth.kakao.com/oauth/authorize?client_id=자신의 rest key값&redirect_uri=https://example.com/oauth&response_type=code
url = 'https://kauth.kakao.com/oauth/token'  
rest_api_key = 'faf4995ab4fd2611dc1316519114a5b8'  # rest_api 
redirect_uri = 'https://example.com/oauth'  
authorize_code = '17FMrSKcLu-5E-gsCRPFhQURDQqeqIx1WPgsFs9dLSoi4_1DdIoKClrRdH-4AuSflkir9gopyNoAAAGKSory-g'  # code

print( rest_api_key)
print( authorize_code)

# ### Refresh token 발췌
# def f_auth():
#     data = {
#         'grant_type': 'authorization_code',
#         'client_id': rest_api_key,
#         'redirect_uri': redirect_uri,
#         'code': authorize_code,
#     }

#     response = requests.post(url, data=data)
#     tokens = response.json()

#     with open("kakao_code.json", "w") as fp:
#         json.dump(tokens, fp)
#     with open("kakao_code.json", "r") as fp:
#         ts = json.load(fp)
#     r_token = ts["refresh_token"]
#     return r_token

# ### Refresh toekn 을 갖고 new Access token 발행
# def f_auth_refresh(r_token):
#     with open("kakao_code.json", "r") as fp:
#         ts = json.load(fp)
#     data = {
#         "grant_type": "refresh_token",
#         "client_id": rest_api_key,
#         "refresh_token": r_token
#     }
#     response = requests.post(url, data=data)
#     tokens = response.json()

#     with open(r"kakao_code.json", "w") as fp:
#         json.dump(tokens, fp)
#     with open("kakao_code.json", "r") as fp:
#         ts = json.load(fp)
#     token = ts["access_token"]
#     return token


# def f_send_talk(token, text):
#     header = {'Authorization': 'Bearer ' + token}
#     url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'  
#     post = {
#         'object_type': 'text',
#         'text': text,
#         'link': {
#             'web_url': 'https://https://developers.kakao.com',
#         },
#         'button_title': '웹으로 이동',
#     }
#     data = {'template_object': json.dumps(post)}
#     return requests.post(url, headers=header, data=data)

# r_token = f_auth()

# while True:
#     token = f_auth_refresh(r_token)  
#     f_send_talk (token, '도난 발생. www.naver.com')
#     time.sleep(1800)