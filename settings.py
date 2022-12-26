import os
from exceptions import ImproperlyConfigured

from dotenv import load_dotenv

load_dotenv()

# Used to log in reddit
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')


#Name of subbredit
SUBREDDIT = 'askReddit'


#Parameters for text-to-speech
LANG = 'en'
TLD = 'ca'


#Path to folder with MP3
AUDIO_FOLDER = 'audio/'