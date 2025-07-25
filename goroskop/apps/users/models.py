from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # extra_fields.setdefault("role", User.SUPERADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        # if extra_fields.get("role") is not User.SUPERADMIN:
        # raise ValueError("Role must have Superadmin.")

        return self._create_user(email, password, **extra_fields)


class ZodiacSign(models.IntegerChoices):
    ARIES = 1, _("Aries — March 21 - April 19")
    TAURUS = 2, _("Taurus — April 20 - May 20")
    GEMINI = 3, _("Gemini — May 21 - June 20")
    CANCER = 4, _("Cancer — June 21 - July 22")
    LEO = 5, _("Leo — July 23 - August 22")
    VIRGO = 6, _("Virgo — August 23 - September 22")
    LIBRA = 7, _("Libra — September 23 - October 22")
    SCORPIO = 8, _("Scorpio — October 23 - November 21")
    SAGITTARIUS = 9, _("Sagittarius — November 22 - December 21")
    CAPRICORN = 10, _("Capricorn — December 22 - January 19")
    AQUARIUS = 11, _("Aquarius — January 20 - February 18")
    PISCES = 12, _("Pisces — February 19 - March 20")


class Language(models.TextChoices):
    ENGLISH = "EN", _("English")
    UKRAINIAN = "UK", _("Ukrainian")


class User(AbstractUser):
    """User model."""

    email = models.EmailField(unique=True, null=True)

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)

    telegram_id = models.BigIntegerField(unique=True, null=True)
    telegram_username = models.CharField(max_length=255, null=True)
    zodiac_sign = models.IntegerField(choices=ZodiacSign.choices, default=ZodiacSign.ARIES)
    language = models.CharField(max_length=5, choices=Language.choices, default=Language.ENGLISH)
    allow_spam = models.BooleanField(default=True)

    def __str__(self):
        if self.email:
            return self.email
        else:
            return f"{self.telegram_username} - {self.telegram_id}"
