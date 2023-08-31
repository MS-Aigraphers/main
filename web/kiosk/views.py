import json
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import Kiosk
from django.shortcuts import render,redirect
from django.utils import timezone



# 데이터를 추가하는 뷰 함수
def index(request):
    new_data = Kiosk(time=timezone.now(), objectcount=1) # objectcount
    new_data.save()
    return render(request, 'kiosk/add_kiosk_data.html')


# Kiosk 테이블의 데이터를 JSON 형태로 반환하는 뷰 함수
def get_kiosk_data(request):
    kiosk_data = Kiosk.objects.all()
    data_list = [{'time': data.time.strftime('%Y-%m-%d %H:%M:%S'), 'objectcount': data.objectcount} for data in kiosk_data]
    kiosk_data_json=JsonResponse(data_list, safe=False)
    return kiosk_data_json






# def data_added(request):
#     if request.method == 'POST':
#         # POST 요청을 받았을 때 처리하는 로직
#         time = timezone.now()  # 현재 시간
#         objectcount = request.POST.get('objectcount', 0)  # POST 데이터에서 objectcount 값을 가져옴
#         Kiosk.objects.create(time=time, objectcount=objectcount)  # Kiosk 테이블에 데이터 추가
#         return redirect('data_added')  # 데이터 추가 후 다시 data_added 페이지로 리다이렉트

#     kiosk_data = Kiosk.objects.all()  # Kiosk 테이블의 모든 데이터를 가져옴
#     context = {'kiosk_data': kiosk_data}
#     return render(request, 'kiosk/data_added.html', context)

# # 추가된 데이터 확인을 위한 뷰 함수
# def data_added(request):
#     return render(request, 'kiosk/add_kiosk_data.html')

# def add_kiosk_data(time, objectcount):
#     kiosk_data = Kiosk(time=time, objectcount=objectcount)
#     kiosk_data.save()

# def index(request):
#     if request.method == 'POST' and 'a' in request.POST:
#         current_time = datetime.now()
#         object_count = 5  # 예시로 설정한 사물 개수
#         add_kiosk_data(current_time, object_count)  # 데이터 추가

#     return render(request, 'add_kiosk_data.html')
    
# def data_added(request):
#     return render(request, 'kiosk/add_kiosk_data.html')

# def save_kiosk_data_to_json(request):
#     kiosk_data = Kiosk.objects.all()  # Kiosk 테이블의 데이터 가져오기

#     # 데이터를 직렬화하여 JSON 파일로 저장
#     data = serialize('json', kiosk_data)
#     data_file_path = 'kiosk_data.json'
#     with open(data_file_path, 'w') as json_file:
#         json_file.write(data)
    
#     return JsonResponse({'message': 'Kiosk data saved to JSON file.'})
