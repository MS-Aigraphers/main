from django.shortcuts import render
from django.http import HttpResponse
from .models import Kiosk
from django.utils import timezone
# Create your views here.

def index(request):
    q = Kiosk(id,store_id=1,name="ramen",price=1000,stock=1, registered_date=timezone.now())
    q.save()
    return HttpResponse(f"{Kiosk.id}{q}{Kiosk.registered_date}")


# 1. kiosk : 라벨(number), 개수(number), 시간(time)
# 2. 정상결제여부 : 튄놈(number), 계산한척(number), 개수안맞은넘(number), 정상결제(number)
# 3. Crossline 총카운트 : 방문자수 (number)
# 4. 안전관리 횟수 : 무기관련(number), 화재관련(number), 소란관련(number)

# <<<<도난 로직에 한해서 작성한 DB 메서드, 홈페이지관리, 무기관리도 따로 작성해야함>>>>>
### Create ####
# create_판매량 (uid, number, number, time) :  라벨, 개수,  시간작성  정상결제시 작성

# create_튄놈 (uid, time) : 시간 작성 kioskzoneenter()에서 작성
# create_계산한척 (uid, time) : 시간 작성 kioskzoneenter()에서 작성
# create_개수안맞은놈 (uid, time) : 시간, 개수
# create_정상결제 (uid, time) : 시간 작성 kioskzoneenter()에서 작성

# create_무기관련 (uid, time) : 시간 작성
# create_화재관련 (uid, time) : 시간 작성

### Update ####
# countup_튄놈 (uid) : + 1 카운트 갱신
# countup_계산한척(uid) : + 1 카운트 갱신
# countup_개수안맞은놈 (uid) : + 1 카운트 갱신
# countup_정상결제 (uid) : + 1 카운트 갱신

# countup_방문자수 (uid) : 크로스라인 넘으면 + 1  (위의 4가지 다 더해도 될듯?)

# countup_무기관련 (uid) : 무기로직 발동시 + 1
# countup_화재관련 (uid) :
# countup_소란관련 (uid) :


### READ ###
# read
# read_kiosk (number, number, time) :   # 라벨, 개수, 시간
# read_안전관리
# read_방문자수



