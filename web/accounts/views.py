from django.shortcuts import render,redirect 
from .models import Account
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm



def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    elif request.method=='POST':
        username=request.POST.get('username',None)
        email=request.POST.get('email',None)
        password=request.POST.get('password',None)
        re_password=request.POST.get('re_password',None)

        err_data={}
        if not(username and email and password and re_password):
            err_data['error']='모든 값을 입력해주세요.'
        elif password != re_password:
            err_data['error']='비밀번호가 다릅니다.'
        else:
            account=Account(
                username=username,
                email=email,
                password=make_password(password)
            )
            account.save()
        return render(request,'register.html',err_data)



# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             request.session['user'] = form.user_id
#             return redirect('/')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

def login(request):
    if request.method =='GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        err_data = {}
        if not(email and password):
            err_data['error'] = '모든 값을 입력해 주세요.'
        else:
            user = Account.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user'] = user.id
                return redirect('/')
            else:
                err_data['error'] = '비밀번호가 일치하지 않습니다.'
        return render(request, 'register.html', err_data)

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')


def home(request):
    user_id = request.session.get('user')
    if user_id:
        user = Account.objects.get(pk = user_id)
        return HttpResponse("Hello! %s님" % user)
    else:
        return HttpResponse("로그인 해주세요!")





# ### 회원가입
# class SignUpView(View):
#     def post(self,request):
#         data=json.loads(request.body)
#         Account(
#             email=data['email'],
#             password=data['password']
#         ).save()

#         return JsonResponse({'message':'회원가입 완료'},status=200)

# ### login
# class SignInView(View):
#     def post(self,request):
#         data=json.loads(request.body)

#         if Account.objects.filter(email=data['email']).exists():
#             user=Account.objects.get(email=data['email'])
#             if user.password==data['password']:
#                 return JsonResponse({'message':f'{user.email}님 로그인 성공!'},status=200)
#             else:
#                 return JsonResponse({'message':'비밀번호가 틀렸습니다'},status=200)

#         return JsonResponse({'message':'등록되지 않은 이메일 입니다. 회원 가입 plz'},status=200)
