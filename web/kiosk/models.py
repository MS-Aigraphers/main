from django.db import models

# Create your models here.
class Kiosk(models.Model):
    id=models.AutoField(primary_key=True, unique=True)


class TodayTraffic(models.Model):
    person_id = models.IntegerField(default=-1, primary_key=True)
    date = models.DateField()
    time = models.TimeField()

    def get_person_id(self):
        return {'person_id': self.person_id}

    def get_month(self):
        return self.date.strftime("%m")