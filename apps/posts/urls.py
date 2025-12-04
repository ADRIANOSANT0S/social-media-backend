from django.urls import include, path
from rest_framework_nested import routers

from apps.comments.viewsets import CommentViewSet
from apps.likes.viewsets import LikeViewSet
from apps.posts.viewsets import PostViewSet

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")

posts_router = routers.NestedDefaultRouter(router, r"posts", lookup="post")
posts_router.register(r"likes", LikeViewSet, basename="post-likes")
posts_router.register(r"comments", CommentViewSet, basename="post-comments")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(posts_router.urls)),
]
