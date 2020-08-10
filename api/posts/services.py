from django.contrib.auth import get_user_model

from apps.posts.models import Like


User = get_user_model()


def add_like(post, user):
    like, is_created = Like.objects.get_or_create(user=user, post=post)
    return like


def remove_like(post, user):
    Like.objects.filter(post=post, user=user).delete()
