from rest_framework import serializers

from goroskop.apps.forecast.models import DailyHoroscope


class HoroscopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyHoroscope
        fields = "__all__"
