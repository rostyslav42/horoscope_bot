from django.contrib import admin

from goroskop.apps.forecast.models import DailyHoroscope


@admin.register(DailyHoroscope)
class DailyHoroscopeAdmin(admin.ModelAdmin):
    list_display = ("zodiac_sign", "date", "id")
