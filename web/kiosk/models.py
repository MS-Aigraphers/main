from django.db import models

class Kiosk(models.Model):
    time = models.DateTimeField()  # 시간 필드
    objectcount = models.IntegerField(default=0)  # 사물 개수 필드

    def __str__(self):
        return f"Kiosk - {self.time} (Objects: {self.objectcount})"
    
    class Meta:
        db_table = 'Kiosk'  # 원하는 테이블명을 설정합니다.

    
