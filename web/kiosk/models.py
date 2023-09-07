from django.db import models


# class Kiosk(models.Model):
#     store_name=models.CharField(max_length=200)
#     #product_label=
#     objectcount = models.IntegerField(default=0)  # 사물 개수 필드
#     time = models.DateTimeField(auto_now_add=True)  # 시간 필드

#     def __str__(self) :
#         return self.store_name
#     class Meta:
#         db_table='Kiosk'
#         verbose_name='Kiosk'   

# label : 갯수 : 시간

# 감지 / models.py : 1. 놈+놈+놈 == > 도난 감지
# 안전 관리 / models.py : 1. 무기 2. 화재  3. 소음
# 방문자 수 (cross line out 으로)

# kiosk/models.py

class Kiosk(models.Model):
    CATEGORY_CHOICES = (
        (1, '아이스크림'),
        (2, '스낵'),
        (3, '음료'),
        (4, '라면'),
    )

    store_name = models.CharField(max_length=200)
    product_label = models.IntegerField(choices=CATEGORY_CHOICES)
    objectcount = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_name
    class Meta:
        db_table='Kiosk'
        verbose_name='Kiosk'  