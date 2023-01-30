import os
from pytube import YouTube
from settings import GAMEPLAY_FOLDER


def download_gameplay(link: str) -> None:
    url = YouTube(link)
    video = url.streams.filter(res="1080p").first()
    title = f"{url.title}.mp4"
    path_to_download_folder = str(os.path.join(GAMEPLAY_FOLDER))

    video.download(output_path=path_to_download_folder, filename=title)



