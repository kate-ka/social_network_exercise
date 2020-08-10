import json

import pytest
from freezegun import freeze_time

from apps.posts.models import Post, Like
from tests.factories import PostFactory, LikeFactory, UserFactory

ANALYTICS_URL = "/api/posts/analytics/"


@pytest.mark.django_db
class TestPostsCrud:
    def detail_url(self, post):
        return f"/api/posts/{post.pk}/"

    def list_url(self):
        return "/api/posts/"

    def like_url(self, post):
        return f"/api/posts/like/{post.pk}/"

    def unlike_url(self, post):
        return f"/api/posts/unlike/{post.pk}/"

    def test_create_post_authorized_returns_201(self, logged_client):
        post_data = {
            "title": "test post",
            "text": "some text here",
        }

        response = logged_client.post(
            self.list_url(),
            data=json.dumps(post_data),
            content_type="application/json",
        )
        assert response.status_code == 201

        response = response.json()

        post = Post.objects.get(id=response["id"])
        assert response["title"] == post_data["title"]
        assert response["text"] == post_data["text"]

        assert response["title"] == post.title
        assert response["text"] == post.text
        assert response["user"]["id"] == post.user.id

    def test_create_post_unauthorized_returns_403(self, api_client):
        post_data = {
            "title": "test post",
            "text": "some text here",
        }

        response = api_client.post(
            self.list_url(),
            data=json.dumps(post_data),
            content_type="application/json",
        )
        assert response.status_code == 401

    def test_retrieve_post_returns_200(self, logged_client, datetime_to_representation):

        post = PostFactory()

        response = logged_client.get(
            self.detail_url(post), content_type="application/json"
        )
        assert response.status_code == 200

        response = response.json()

        assert response["title"] == post.title
        assert response["user"]["id"] == post.user.id
        assert response["created"] == datetime_to_representation(post.created)
        assert response["updated"] == datetime_to_representation(post.updated)

    def test_patch_post_authorized_returns_200(self, logged_client):
        post = PostFactory(user=logged_client.user)
        post_data = {"title": "New test title"}
        response = logged_client.patch(
            self.detail_url(post),
            data=json.dumps(post_data),
            content_type="application/json",
        )
        assert response.status_code == 200
        response = response.json()

        assert response["title"] == post_data["title"]

        post.refresh_from_db()
        assert post.title == post_data["title"]

    def test_patch_others_user_post_returns_403(self, logged_client):
        post = PostFactory()

        response = logged_client.patch(
            self.detail_url(post),
            data=json.dumps({"title": "New title"}),
            content_type="application/json",
        )

        assert response.status_code == 403

    def test_list_posts_returns_200(self, logged_client):
        post1 = PostFactory(user=logged_client.user)
        post2 = PostFactory()
        LikeFactory(post=post1)
        LikeFactory(post=post2, user=logged_client.user)

        response = logged_client.get(self.list_url(), content_type="application/json",)
        assert response.status_code == 200

        assert len(response.json()) == 2

    def test_like_post_returns_204(self, logged_client):
        post = PostFactory()

        response = logged_client.post(
            self.like_url(post), content_type="application/json"
        )
        assert Like.objects.filter(post=post, user=logged_client.user).exists()

        assert response.status_code == 204

    def test_unlike_post_returns_204(self, logged_client):
        post = PostFactory()
        LikeFactory(post=post, user=logged_client.user)
        assert Like.objects.filter(post=post, user=logged_client.user).exists()
        response = logged_client.post(
            self.unlike_url(post), content_type="application/json"
        )
        assert response.status_code == 204
        assert Like.objects.filter(post=post, user=logged_client.user).count() == 0

    def test_post_analytics_returns_200(self, logged_client):
        post_1 = PostFactory()
        post_2 = PostFactory()
        post_3 = PostFactory()
        post_4 = PostFactory()
        with freeze_time("2020-08-08"):
            LikeFactory(post=post_1, user=logged_client.user)
        LikeFactory(post=post_2, user=logged_client.user)
        LikeFactory(post=post_3, user=logged_client.user)
        LikeFactory(post=post_3)
        response = logged_client.get(ANALYTICS_URL, content_type="application/json")
        assert response.status_code == 200
        assert response.json() == [
            {"likes_count": 1, "date": "2020-08-08", "post": 1},
            {"likes_count": 1, "date": "2020-08-09", "post": 2},
            {"likes_count": 2, "date": "2020-08-09", "post": 3},
        ]

    def test_post_analytics_filter_by_date_returns_200(self, logged_client):
        post_1 = PostFactory()
        post_2 = PostFactory()
        post_3 = PostFactory()
        with freeze_time("2019-08-08"):
            LikeFactory(post=post_1, user=logged_client.user)
            LikeFactory(post=post_2, user=logged_client.user)
        LikeFactory(post=post_3)
        response = logged_client.get(
            ANALYTICS_URL,
            data={"created_before": "2020-08-09", "created_after": "2020-01-01"},
            content_type="application/json",
        )
        assert response.status_code == 200
        response = response.json()
        assert len(response) == 1
        assert response[0]["date"] == "2020-08-09"
