from django.shortcuts import render
from django.http import HttpResponse
from .models import Kiosk
from django.utils import timezone
# Create your views here.

def index(request):
    q = Kiosk(id,store_id=1,name="ramen",price=1000,stock=1, registered_date=timezone.now())
    q.save()
    return HttpResponse(f"{Kiosk.id}{q}{Kiosk.registered_date}")