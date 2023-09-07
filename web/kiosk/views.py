import json
from django.core.serializers import serialize
from .models import Kiosk
from django.shortcuts import render,redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponse,JsonResponse
# payment_time_fromDB = kiosk.views.결제시도_메소드  # 결제시도 시각 TODO : 데이터 변경 필요
# obj_cnt_fromDB = kiosk.views.바코드물건갯수_메소드  # 바코드에 찍힌 물건의 갯수


# 데이터를 추가하는 뷰 함수
def add_data(request):
    if request.method=='GET':
        return render(request,'add_data_kiosk.html')
    elif request.method=='POST':
        store_name=request.POST.get('store_name',None)
        objectcount = request.POST.get('objectcount',None)  # 사물 개수 필드
        product_label = request.POST.get('product_label', None)  # 상품 종류 필드

        err_data={}
        if not(store_name and objectcount):
            err_data['error']='모든 값을 입력해주세요.'
        else:
            kiosk=Kiosk(
                store_name=store_name,
                product_label=product_label,
                objectcount=objectcount,
                time=timezone.now()
            )
            kiosk.save()
        return render(request,'add_data_kiosk.html',err_data)


def try_payment(request):
    # Kiosk 모델에서 결제시도 시각 정보를 가져옵니다.
    item_counts = Kiosk.objects.values_list('objectcount', flat=True)  # 갯수 정보만 가져옴
    payment_times = Kiosk.objects.values_list('time', flat=True)  # 시각 정보만 가져옴

    # 결과를 화면에 출력하거나 다른 처리를 수행할 수 있습니다.
    for payment_time in payment_times:
        print(payment_time)
    for item_count in item_counts:
        print(item_count)
    # 데이터를 템플릿에 전달하여 렌더링합니다.
    return render(request, 'show_data.html', {'payment_times': payment_times,'item_counts': item_counts})



def get_object_data():
    try:
        # 데이터베이스에서 원하는 물건 종류와 갯수를 가져옵니다.
        kiosk_data = Kiosk.objects.get(store_name='가게 이름')  # 가게 이름에 따라 필터링
        object_name = kiosk_data.product_label()  # 물건 종류 표시
        object_count = kiosk_data.objectcount  # 물건 갯수
        time=kiosk_data.time(timezone.now())
        return object_name, object_count,time
    except Kiosk.DoesNotExist:
        return None, None


