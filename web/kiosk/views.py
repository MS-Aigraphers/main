from django.shortcuts import render
from .models import Kiosk
from django.utils import timezone
from django.http import HttpResponse

def index(request):
    return HttpResponse("hello")


def save_kiosk_data(request):
    current_time = timezone.now()
    object_count = 2  # 변경 가능한 값으로 설정하세요
    
    kiosk_entry = Kiosk.objects.create(time=current_time, objectcount=object_count)
    kiosk_entry.save()
    
    return HttpResponse("Kiosk data saved successfully.")
