from django.db import models

# Create your models here.
class Account(models.Model):
    username=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    password=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True) # 처음 생성된 시점을 자동으로 기록
    updated_at=models.DateTimeField(auto_now=True)     # 필드가 업데이트 될 때마다 그 시점을 기록

    def __str__(self) :
        return self.username
    class Meta:
        db_table='account_user'
        verbose_name='계정 정보'