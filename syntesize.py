from gtts import gTTS
from settings import TLD, LANG, AUDIO_FOLDER
import os

def syntesize(text:str, filename:str):
    filename = f'{filename}.mp3'
    tts = gTTS(text, lang=LANG, tld=TLD)
    tts.save(os.path.join(AUDIO_FOLDER, filename))
    return filename

if __name__ == "__main__":
    syntesize('hello world', 'test')
