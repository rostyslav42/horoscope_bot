from datetime import date

from celery import shared_task

from goroskop.apps.forecast.models import DailyHoroscope
from utils.horoscope_api import get_forecast_from_api
from utils.translator import translate


@shared_task()
def get_forecasts():
    today = date.today()
    print(f"Start getting forecast {today}")
    get_forecast_from_api()
    print("Got forecast")


@shared_task()
def translate_text():
    today = date.today()
    print(f"Start translating text {today}")
    for horoscope in DailyHoroscope.objects.filter(date=today).iterator():
        text = translate(horoscope.text_en)
        horoscope.text_uk = text
        horoscope.save()
    print("finished translation")
