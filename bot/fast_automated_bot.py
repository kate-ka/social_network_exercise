import json
import os
import random
from concurrent.futures.thread import ThreadPoolExecutor
from time import time
from itertools import chain

import requests
from faker import Faker

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conf.json")

HOST = "http://127.0.0.1:8000"

SIGNIN_URL = f"{HOST}/api/auth/login/"
SIGNUP_URL = f"{HOST}/api/auth/signup/"

POST_URL = f"{HOST}/api/posts/"
LIKE_POST_URL = f"{HOST}/api/posts/like"


def read_config():
    with open(CONFIG_PATH, "r") as config_file:
        confs = json.loads(config_file.read())
        return confs


confs = read_config()


class UserBot:
    def __init__(self, username, password="password"):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def __str__(self):
        return self.username

    def is_authorized(self):
        assert "Authorization" in self.session.headers

    def signin(self):
        response = requests.post(
            SIGNIN_URL, data={"username": self.username, "password": self.password}
        )
        is_ok = True if response.status_code == 200 else False
        if is_ok:
            self.access_token = response.json()["access"]
            self.session.headers.update(
                {"Authorization": "Bearer {}".format(self.access_token)}
            )
        else:
            print(
                "Error during getting a token by user {user}. Status code is {code}. Error is {error}".format(
                    user=self.username,
                    code=response.status_code,
                    error=response.content,
                )
            )
        return is_ok

    def signup(self, sign_in=True):
        print("Trying to sign up user {}".format(self.username))
        data = {"username": self.username, "password": self.password}
        try:
            response = requests.post(SIGNUP_URL, data=data)
        except requests.exceptions.ConnectionError:
            print("Connection error.")
            return False

        is_ok = response.status_code == 201
        if is_ok and sign_in:
            self.signin()
        if not is_ok:
            print(
                f"Error signing up {self.username}. Status code is {response.status_code}."
                f"Error is {response.content}"
            )
        else:
            print(f"Successfully signed up user {self.username}")
        return is_ok

    def create_post(self, data):
        self.is_authorized()
        print(f"Trying to create post by user {self.username}")
        response = self.session.post(POST_URL, data=data)
        is_ok = response.status_code == 201
        if is_ok:
            print(f"Successfully created post by user {self.username}")
        else:
            print(
                f"Error during creating post by user {self.username}."
                f" Status code is {response.status_code}. Error {response.content}"
            )
            return None

        return response.json()

    def like_post(self, post):
        self.is_authorized()
        print(f"Trying to like post {post['id']}.")
        response = self.session.post(f"{LIKE_POST_URL}/{post['id']}/")
        is_ok = response.status_code == 204

        if is_ok:
            print(f"Successfully like post {post['id']}.")
        else:
            print(
                f"Failed to like post {post['id']} by user {self.username}. "
                f"Status code is {response.status_code}. Error {response.content}"
            )
        return is_ok


def get_signed_up_users(user):
    result = user.signup()
    if result:
        return user


def create_post(user):
    faker = Faker()
    post = user.create_post(data={"text": faker.text(200), "title": faker.text(100)})

    return post


def create_random_number_of_posts(user):
    max_posts_per_user = confs["max_posts_per_user"]
    post_count = random.randint(1, max_posts_per_user)

    with ThreadPoolExecutor(max_workers=10) as executor:
        posts = [
            post for post in executor.map(create_post, [user] * post_count) if post
        ]

    return posts


def like_posts_randomly(user, posts):
    random.shuffle(posts)
    posts_to_like = posts[: random.randint(1, confs["max_likes_per_user"])]

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(user.like_post, posts_to_like)


def run_bot():
    start = time()
    faker = Faker()
    users = []

    for _ in range(confs["number_of_users"]):
        email = faker.email()
        user = UserBot(username=email)
        users.append(user)

    with ThreadPoolExecutor(max_workers=10) as executor:
        signed_up_users = [
            user
            for user in executor.map(get_signed_up_users, users)
            if user is not None
        ]

    with ThreadPoolExecutor(max_workers=10) as executor:
        posts = list(
            chain.from_iterable(
            executor.map(create_random_number_of_posts, signed_up_users)
        ))

    for user in signed_up_users:
        like_posts_randomly(user, list(posts))

    print(f"Took {time() - start}")


if __name__ == "__main__":

    run_bot()
