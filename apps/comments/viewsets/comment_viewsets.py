from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer
from apps.core.backends import CookieJWTAuthentication, IsOwnerOrReadOnly
from apps.posts.models import Post


class CommentViewSet(ModelViewSet):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_pk")
        post_obj = get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post_obj)

    def get_queryset(self):
        post_id = self.kwargs.get("post_pk")

        if post_id:
            return Comment.objects.filter(post_id=post_id)

        return Comment.objects.all()
