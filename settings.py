import os
from dotenv import load_dotenv

load_dotenv()

NUMBER_OF_USERS = int(os.getenv('NUMBER_OF_USERS'))
MAX_POSTS_PER_USER = int(os.getenv('MAX_POSTS_PER_USER'))
MAX_LIKES_PER_USER = int(os.getenv('MAX_LIKES_PER_USER'))
SERVICE_ADDRESS = os.getenv('SERVICE_ADDRESS')
SERVICE_PORT = os.getenv('SERVICE_PORT')

SERVICE_URL = f'http://{SERVICE_ADDRESS}:{SERVICE_PORT}'
