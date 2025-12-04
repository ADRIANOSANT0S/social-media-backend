from django.db import models


class Comment(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user} on post {self.post.id}"
