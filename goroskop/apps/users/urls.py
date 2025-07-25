from rest_framework.routers import DefaultRouter

from goroskop.apps.users.views import UserViewSet

router = DefaultRouter()

router.register("user", UserViewSet)

urlpatterns = [] + router.urls
