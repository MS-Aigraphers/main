from django.contrib import admin
from .models import Kiosk

@admin.register(Kiosk)
class KioskAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'objectcount', 'time')  # Admin 페이지에서 보여줄 필드 설정
