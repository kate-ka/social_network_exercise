from django.core.cache import cache
from django.db.models import Count
from django.db.models.functions import TruncDate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from api.posts.filters import LikeFilter
from api.posts.permissions import AllowAuthorEditPost
from apps.posts.models import Post, Like
from api.posts.serializers import PostSerializer, LikeAnalyticsSerializer

import api.posts.services as posts_services


class RetrievePostView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, AllowAuthorEditPost)
    serializer_class = PostSerializer


class ListCreatePostView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = super(ListCreatePostView, self).get_queryset()

        return queryset.prefetch_likes()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikePostView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(self.queryset, id=kwargs.get("post_id"))
        posts_services.add_like(user=request.user, post=post)
        return Response(status=HTTP_204_NO_CONTENT)


class UnlikePostView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(self.queryset, id=kwargs.get("post_id"))
        posts_services.remove_like(user=request.user, post=post)
        return Response(status=HTTP_204_NO_CONTENT)


class LikeListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LikeAnalyticsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LikeFilter

    def get_queryset(self):
        return (
            Like.objects.annotate(date=TruncDate("created"))
            .values("date", "post")
            .annotate(likes_count=Count("id"))
            .order_by("date")
        )
