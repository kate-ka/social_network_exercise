from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class PostQueryset(models.QuerySet):
    def prefetch_likes(self):
        return self.prefetch_related(
            models.Prefetch("likes", to_attr="_likes_prefetch")
        )


class Post(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = PostQueryset.as_manager()

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Post created by {self.user}."

    @property
    def likes_count(self):
        if hasattr(self, "_likes_prefetch"):
            return len(self._likes_prefetch)

        return Like.objects.filter(post=self).count()

    def is_liked_by_user(self, user):
        if hasattr(self, "_likes_prefetch"):
            return any(like.user.id == user.id for like in self._likes_prefetch)

        return self.likes.filter(user=user).exists()


class Like(models.Model):
    post = models.ForeignKey("Post", related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)
        unique_together = (("post", "user"),)

    def __str__(self):
        return f"{self.created} / {self.post_id}"
