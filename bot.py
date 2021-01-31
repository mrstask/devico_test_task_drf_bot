import random

import requests

from settings import SERVICE_URL, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER, NUMBER_OF_USERS
from faker import Faker

fake = Faker()


def make_request(method: str, service: str, params: dict = None, data: dict = None, item_id: int = None,
                 headers: dict = None):
    response = requests.request(method,
                                f"{SERVICE_URL}/api/v1/{service}/{item_id}",
                                headers=headers,
                                params=params,
                                data=data,
                                )
    if response.status_code not in [200, 201]:
        raise requests.exceptions.HTTPError


class BotActions:
    def __init__(self):
        self.users = {}
        self.posts = []

    def create_fake_users(self, number: int):
        for _ in range(number):
            self.users[fake.profile()['username']] = {'email': fake.email(), 'password': fake.password()}

    def signup_users(self):
        """signup created_users (number provided in config)"""
        for username, user_data in self.users.items():
            make_request(method='post', service='account', data={'username': username,
                                                                 'email': user_data['mail'],
                                                                 'password': user_data['password']})
            # res = requests.post(f"{SERVICE_URL}/api/v1/account/", data={'username': user['username'],
            #                                                             'email': user['mail'],
            #                                                             'password': user['ssn']})
            # if res.status_code != 201:
            #     raise Exception(res.status_code)

    def authenticate_users(self):
        for username, user_data in self.users.items():
            auth_data = requests.post(f"{SERVICE_URL}/api/v1/token/", data={'username': username,
                                                                            'password': user_data['password']})
            self.users[username].update(auth_data)

    def create_posts(self, max_posts_per_user: int):
        """each user creates random number of created_posts with any content
         (up to max_posts_per_user)"""
        for user_data in self.users.values():
            for _ in range(random.randint(1, max_posts_per_user)):
                post_data = make_request(method='post',
                                         service='post',
                                         headers={'Authorization': f"Bearer {user_data['access']}"})
                # post = requests.post(f"{SERVICE_URL}/api/v1/post/",
                #                      headers={'Authorization': f"Bearer {auth.json()['access']}"},
                #                      data={'title': user['username'], 'description': user['job'],
                #                            'text': user['company']})
                # if post.status_code == 201:
                #     self.posts.append(post.json())

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
