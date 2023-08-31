from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
    path('get_kiosk_data/', views.get_kiosk_data, name='get_kiosk_data'),
]
