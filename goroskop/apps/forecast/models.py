from django.db import models

from goroskop.apps.users.models import ZodiacSign


# Create your models here.
class DailyHoroscope(models.Model):
    date = models.DateField()
    zodiac_sign = models.PositiveSmallIntegerField(choices=ZodiacSign.choices)
    text_uk = models.TextField()
    text_en = models.TextField()

    class Meta:
        unique_together = ("date", "zodiac_sign")

    def __str__(self):
        print(dir(self.zodiac_sign))
        print(self.zodiac_sign)
        print(self.zodiac_sign)
        print(self.zodiac_sign)
        return f"{ZodiacSign(self.zodiac_sign).name}"
