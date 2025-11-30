from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.backends import CookieJWTAuthentication
from apps.follows.models import Follow
from apps.posts.models import Post
from apps.posts.serializers.post_serializer import PostSerializer


class PostListView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get(self, request):
        user = request.user
        following_user_ids = Follow.objects.filter(follower=user).values_list(
            "following_id", flat=True
        )
        posts = Post.objects.filter(user__in=list(following_user_ids) + [user.id])

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request)

        if page is not None:
            serializer = PostSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
