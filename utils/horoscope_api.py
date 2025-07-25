import os
from datetime import date

import requests

from goroskop.apps.forecast.models import DailyHoroscope
from goroskop.constants import ZODIAC_LIST


def get_forecast_from_api():
    url = os.getenv("HOROSCOPE_API")
    today = date.today()

    for number, sign in enumerate(ZODIAC_LIST, start=1):
        payload = {"sign": sign, "day": "TODAY"}
        r = requests.get(url, params=payload)
        data = r.json()["data"]
        DailyHoroscope.objects.create(
            # date=today.isoformat(),
            date=today,
            zodiac_sign=number,
            text_en=data["horoscope_data"],
        )
