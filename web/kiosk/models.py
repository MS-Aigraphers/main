from django.db import models
from django.utils import timezone

# Create your models here.
class Kiosk(models.Model):
    id=models.AutoField(primary_key=True, unique=True)
    store_id=models.IntegerField(models.ForeignKey("app.Model", on_delete=models.CASCADE))
    name = models.CharField(max_length = 32, verbose_name="상품명")
    price = models.IntegerField(verbose_name = "상품가격")
    stock = models.IntegerField(verbose_name="수량")
    registered_date = models.DateTimeField(verbose_name="등록시간", auto_now_add=timezone.now)

    # def get_name(self):
    #     return {'person_id': self.name,'price':self.price,'stock':self.stock}

    # def get_date(self):
    #     return self.registered_date

    # def __str__(self):
    #     return self.name
    

    class Meta:
        db_table = "kiosk"
        verbose_name = "상품"
        verbose_name_plural = "상품"



