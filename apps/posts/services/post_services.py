from typing import Optional

from apps.posts.models import Post


class PostServices:
    @staticmethod
    def create_post(data: dict) -> Post:
        pass

    @staticmethod
    def get_post(post_id: int) -> Optional[Post]:
        pass

    @staticmethod
    def update_post(post: Post, data: dict) -> Post:
        pass

    @staticmethod
    def delete_post(post: Post) -> None:
        pass
