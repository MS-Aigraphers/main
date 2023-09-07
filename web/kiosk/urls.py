from django.urls import path
from .views import add_data,try_payment


urlpatterns = [
    path('add_data/', add_data, name='add_data'),
    path('try_payment/', try_payment, name='try_payment'),
]
