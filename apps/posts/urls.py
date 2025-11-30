from django.urls import path

from apps.posts.viewset import PostListView

urlpatterns = [
    path("", PostListView.as_view(), name="posts"),
]
