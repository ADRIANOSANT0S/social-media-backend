from django.urls import path

from apps.follows.views import FollowViewSets

urlpatterns = [
    path("", FollowViewSets.as_view(), name="follows"),
]
