import os
from TTS.api import TTS

def syntesize(text:str, path: str, filename:str):
    # Init TTS with the target model name
    filename = f'{filename}.mp3'
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
    tts.tts_to_file(text=text, file_path=os.path.join(path, filename))
