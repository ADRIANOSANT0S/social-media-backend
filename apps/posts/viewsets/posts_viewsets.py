from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.core.backends import CookieJWTAuthentication, IsOwnerOrReadOnly
from apps.follows.models import Follow
from apps.posts.models import Post
from apps.posts.serializers.post_serializer import PostSerializer


class PostViewSet(ModelViewSet):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = PageNumberPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        following_user_ids = Follow.objects.filter(follower=user).values_list(
            "following_id", flat=True
        )
        return Post.objects.filter(user__in=list(following_user_ids) + [user.id])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
