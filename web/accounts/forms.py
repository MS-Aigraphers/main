from django import forms
from .models import Account
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    email=forms.EmailField(
        error_messages={
            'required':'아이디를 입력해주세요'
        }, max_length=200,label='사용자 이메일')
    password=forms.CharField(
        error_messages={
            'required':'비밀번호를 입력해주세요'
        }, widget=forms.PasswordInput,label='비밀번호')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = Account.objects.get(email=email)
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀립니다.')
            else:
                self.user_id = user.id