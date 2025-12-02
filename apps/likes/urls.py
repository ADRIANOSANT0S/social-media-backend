# apps/likes/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.likes.viewsets import LikeViewSet

router = DefaultRouter()
router.register(r"", LikeViewSet, basename="like")

urlpatterns = [
    path("", include(router.urls)),
]
