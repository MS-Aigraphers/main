from django.urls import path
from .views import home,register,login,logout



urlpatterns = [
    path('home/',home,name='home'),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
]









# from django.urls import path
# from .views import SignUpView,SignInView
# urlpatterns = [
#     path('register',SignUpView.as_view()),
#     path('signin',SignInView.as_view()),
# ]
