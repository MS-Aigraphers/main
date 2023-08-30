from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('save_kiosk_data/', views.save_kiosk_data, name='save_kiosk_data'),

]
