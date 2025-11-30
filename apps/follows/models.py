from django.core.exceptions import ValidationError
from django.db import models


class Follow(models.Model):
    follower = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="followings"
    )
    following = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("User cannot follow himself.")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
