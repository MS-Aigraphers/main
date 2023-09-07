#          https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code&scope=talk_message,friends


import requests
import json


url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = '9a7d89ac3d8ceb44c98f12258b979905'
redirect_uri = 'https://localhost:5000'
authorize_code = 'ZxUER6LCnDID8P-hBE4NoZHLtSxTIJCdt6_fPcOVAdH19axGP5OE-zLWJhG3scn2Ts3oYworDR4AAAGKaetBSQ'
data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)


with open("kakao_code1234.json","w") as fp:
    json.dump(tokens, fp)


with open("kakao_code1234.json","r") as fp:
    tokens = json.load(fp)




friend_url = "https://kapi.kakao.com/v1/api/talk/friends"

# GET /v1/api/talk/friends HTTP/1.1
# Host: kapi.kakao.com
# Authorization: Bearer {ACCESS_TOKEN}

headers={"Authorization" : "Bearer " + tokens["access_token"]}

result = json.loads(requests.get(friend_url, headers=headers).text)

print(type(result))
print("=============================================")
print(result)
print("=============================================")
friends_list = result.get("elements")
print(friends_list)
# print(type(friends_list))
print("=============================================")
print(friends_list[0].get("uuid"))
friend_id = friends_list[0].get("uuid")
print(friend_id)