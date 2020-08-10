from rest_framework import serializers

from apps.posts.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "text",
            "user",
            "created",
            "updated",
            "like_count",
            "is_liked",
        )
        read_only_fields = ("user", "like_count", "is_liked")

    def get_is_liked(self, post) -> bool:
        return post.is_liked_by_user(self.context["request"].user)

    def get_like_count(self, post):
        return post.likes_count

    def get_user(self, post):
        return {"id": post.user.id, "email": post.user.email}


class LikeAnalyticsSerializer(serializers.Serializer):
    likes_count = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ("id", "likes_count", "date", "post")

    def get_likes_count(self, like):
        return like.get("likes_count")

    def get_date(self, like):
        return like.get("date")

    def get_post(self, like):
        return like.get("post")
