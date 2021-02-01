import random

from helpers import make_request, like_post
from settings import MAX_POSTS_PER_USER, MAX_LIKES_PER_USER, NUMBER_OF_USERS
from faker import Faker

fake = Faker()


class BotActions:
    def __init__(self, number_of_users: int, max_posts_per_user: int, max_likes_per_user: int):
        self.number_of_users = number_of_users
        self.max_likes_per_user = max_likes_per_user
        self.max_posts_per_user = max_posts_per_user
        self.users = dict()
        self.posts = dict()

    def generate_users_data(self):
        """Populate self.users with generated fake user data in amount of passed number_of_users value"""
        for _ in range(self.number_of_users):
            self.users[fake.profile()['username']] = {'email': fake.email(), 'password': fake.password()}

    def signup_users(self):
        """Signup users from self.users"""
        for username, user_data in self.users.items():
            make_request(method='post', service='account', data={'username': username,
                                                                 'email': user_data['email'],
                                                                 'password': user_data['password']})

    def authenticate_users(self):
        """Authenticate previously signed up users"""
        for username, user_data in self.users.items():
            auth_data = make_request('post', 'token', data={'username': username, 'password': user_data['password']})
            self.users[username].update(auth_data)

    def create_users(self):
        """Generate, signup and authenticate users, all this actions will update self.users"""
        self.generate_users_data()
        self.signup_users()
        self.authenticate_users()

    def create_posts(self,):
        """Create posts for each user in self.users in amount of value set in self.max_posts_per_user"""
        for user_data in self.users.values():
            for _ in range(random.randint(1, self.max_posts_per_user)):
                self.create_post(user_data['access'])

    def create_post(self, access_key):
        """Fake title, description, and text for post creation. """
        text = fake.text()
        post_data = make_request(method='post',
                                 service='post',
                                 headers={'Authorization': f"Bearer {access_key}"},
                                 data={'title': ' '.join(text.split(' ')[:10]),
                                       'description': ' '.join(text.split(' ')[:20]),
                                       'text': text})
        post_id = post_data.pop('id')
        self.posts[post_id] = post_data

    def like_posts(self):
        """After creating the signup and posting activity,
         created_posts should be liked randomly,
         created_posts can be liked multiple times"""
        for user in self.users.values():
            for _ in range(random.randint(1, self.max_likes_per_user)):
                like_post(user['access'], random.choice(list(self.posts.keys())))


if __name__ == '__main__':
    bot = BotActions(NUMBER_OF_USERS, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER)
    bot.create_users()
    bot.create_posts()
    bot.like_posts()
