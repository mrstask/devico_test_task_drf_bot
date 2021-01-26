# Automated bot

- number_of_users
- max_posts_per_user
- max_likes_per_user

Bot should read the configuration and create this activity:

- signup users (number provided in config)
- each user creates random number of posts with any content (up to max_posts_per_user)
- After creating the signup and posting activity, posts should be liked randomly, posts can be liked multiple times

To start application you need:
- 1) install requirements
- 2) create .env file with content
- NUMBER_OF_USERS=10
- MAX_POSTS_PER_USER=10
- MAX_LIKES_PER_USER=10 
- SERVICE_ADDRESS=127.0.0.1
- SERVICE_PORT=8000
- 3) Run bot.py 