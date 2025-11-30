from django.db import models


class Post(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    blocks = models.JSONField(null=False, blank=False, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post by {self.user} at {self.created_at}"
