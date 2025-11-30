from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.backends import CookieJWTAuthentication
from apps.follows.models import Follow
from apps.follows.serializers import FollowCreateSerializer, FollowSerializer


class FollowViewSets(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List followers and following or by type of authenticated user."""

        follow_type = request.query_params.get("type")

        if not follow_type:
            # Sem query param type: retorna seguidores e seguindo juntos
            followers = Follow.objects.filter(following=request.user)
            following = Follow.objects.filter(follower=request.user)

            data = {
                "followers": FollowSerializer(followers, many=True).data,
                "following": FollowSerializer(following, many=True).data,
            }
            return Response(data, status=status.HTTP_200_OK)

        if follow_type not in ["follower", "following"]:
            return Response(
                {"detail": "type must be 'follower' or 'following'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if follow_type == "follower":
            queryset = Follow.objects.filter(following=request.user)
        else:
            queryset = Follow.objects.filter(follower=request.user)

        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a following relationship."""

        serializer = FollowCreateSerializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        follow = serializer.save(follower=request.user)

        return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        """Unfollow a user (delete follow relationship)."""

        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response(
                {"detail": "Query param 'user_id' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow = Follow.objects.filter(
            follower=request.user, following_id=user_id
        ).first()

        if not follow:
            return Response(
                {"detail": "Follow relationship not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
