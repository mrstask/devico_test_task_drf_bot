import random

import requests

from settings import SERVICE_URL, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER, NUMBER_OF_USERS
from faker import Faker


fake = Faker()


def signup_users():
    """signup created_users (number provided in config)"""
    users = [fake.profile() for _ in range(NUMBER_OF_USERS)]
    for user in users:
        res = requests.post(f"{SERVICE_URL}/api/v1/account/", data={'username': user['username'],
                                                                    'email': user['mail'],
                                                                    'password': user['ssn']})
        if res.status_code != 201:
            raise Exception(res.status_code)
    return users


def create_posts(users: list):
    """each user creates random number of created_posts with any content
     (up to max_posts_per_user)"""
    posts = []
    for user in users:
        auth = requests.post(f"{SERVICE_URL}/api/v1/token/", data={'username': user['username'],
                                                                   'password': user['ssn']})
        for _ in range(random.randint(1, MAX_POSTS_PER_USER)):
            post = requests.post(f"{SERVICE_URL}/api/v1/post/",
                                 headers={'Authorization': f"Bearer {auth.json()['access']}"},
                                 data={'title': user['username'], 'description': user['job'], 'text': user['company']})
            if post.status_code == 201:
                posts.append(post.json())
    return posts


def like_posts(users: list, posts: list):
    """After creating the signup and posting activity,
     created_posts should be liked randomly,
     created_posts can be liked multiple times"""

    for user in users:
        auth = requests.post(f"{SERVICE_URL}/api/v1/token/", data={'username': user['username'],
                                                                   'password': user['ssn']})
        for _ in range(random.randint(1, MAX_LIKES_PER_USER)):
            requests.patch(f"{SERVICE_URL}/api/v1/post/{random.choice(posts)['id']}/",
                           headers={'Authorization': f"Bearer {auth.json()['access']}"},
                           data={'is_like': 'true'})


if __name__ == '__main__':
    created_users = signup_users()
    created_posts = create_posts(created_users)
    like_posts(created_users, created_posts)
