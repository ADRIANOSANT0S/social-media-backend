from django.db import models


class Like(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="likes"
    )
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"], name="unique_user_post_like"
            )
        ]

    def __str__(self):
        return f"Like by {self.user} on post {self.post.id}"
