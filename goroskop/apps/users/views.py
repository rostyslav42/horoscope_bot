from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from goroskop.apps.users.models import User
from goroskop.apps.users.serializers import UserSerializer
from goroskop.constants import LANGUAGES


class UserViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        telegram_id = request.data.get("telegram_id")
        defaults = {
            "language": LANGUAGES.get(request.data.get("language"), "EN"),
            "zodiac_sign": request.data.get("zodiac_sign"),
            "telegram_username": request.data.get("telegram_username"),
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
        }
        print(telegram_id)
        print(defaults)
        user, created = User.objects.update_or_create(telegram_id=telegram_id, defaults=defaults)

        serializer = self.get_serializer(user)
        print("end")
        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
