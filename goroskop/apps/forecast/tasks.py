from datetime import date

from celery import shared_task

from utils.horoscope_api import get_forecast_from_api


@shared_task()
def get_forecasts():
    today = date.today()
    print(f"Start getting forecast {today}")
    get_forecast_from_api()
    print("Got forecast")
