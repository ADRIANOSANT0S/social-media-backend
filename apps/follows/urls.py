from django.urls import path

from apps.follows.viewsets import FollowViewSets

urlpatterns = [
    path("", FollowViewSets.as_view(), name="follows"),
]
