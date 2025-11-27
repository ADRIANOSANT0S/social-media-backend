# apps/users/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import UserMeAPIView, UserRegisterViewSet

router = DefaultRouter()
router.register(r"register", UserRegisterViewSet, basename="user-register")

urlpatterns = [
    path("", include(router.urls)),
    path("me/", UserMeAPIView.as_view(), name="user-me"),
]
