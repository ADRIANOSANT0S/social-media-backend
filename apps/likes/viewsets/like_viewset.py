from django.db import IntegrityError
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.likes.models import Like
from apps.likes.serializers import LikeSerializer
from apps.users.serializers import UserSimpleSerializer


class LikeViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"])
    def toggle(self, request, post_pk=None):
        if not post_pk:
            return Response(
                {"detail": "post_pk is required in URL."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        like = Like.objects.filter(user=user, post_id=post_pk).first()

        if like:
            like.delete()
            return Response(
                {"detail": "Like removed."}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            try:
                new_like = Like.objects.create(user=user, post_id=post_pk)
                serializer = LikeSerializer(new_like)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"detail": "You have already liked this post."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(detail=False, methods=["get"])
    def post_likes(self, request, post_pk=None):
        if not post_pk:
            return Response(
                {"detail": "post_pk is required in URL."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        likes = Like.objects.filter(post_id=post_pk).select_related("user")
        total_likes = likes.count()
        users = [like.user for like in likes]
        users_serializer = UserSimpleSerializer(users, many=True)

        return Response(
            {
                "total_likes": total_likes,
                "users": users_serializer.data,
            }
        )
