import os
from dotenv import load_dotenv

load_dotenv()

# Used to log in reddit
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')

#Name of subbredits
ASKREDDIT = 'askReddit'
TRUEOFFMYCHEST = 'TrueOffMyChest'

#Path to folder with gameplay (background video)
GAMEPLAY_FOLDER = 'gameplay'

#Path to folder with MP3
AUDIO_FOLDER_ASKREDDIT = 'audio/AskReddit'
AUDIO_FOLDER_TRUEOFFMYCHEST = 'audio/TrueOffMyChest'

#Path to folder with ready videos 
VIDEO_FOLDER_ASKREDDIT = 'video/AskReddit'
VIDEO_FOLDER_TRUEOFFMYCHEST = "video/TrueOffMyChest"

#Path to folder with screenshots
SCREENSHOT_FOLDER_ASKREDDIT = 'screenshots/AskReddit'
SCREENSHOT_FOLDER_TRUEOFFMYCHEST = 'screenshots/TrueOffMyChest'

#Database credentials
DATABASE_USER=os.getenv('DATABASE_USER')
DATABASE_PWD=os.getenv('DATABASE_PWD')
DATABASE_LOCATION=os.getenv('DATABASE_LOCATION')
DATABASE_NAME=os.getenv('DATABASE_NAME')