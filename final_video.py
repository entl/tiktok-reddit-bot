import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip, CompositeAudioClip, AudioFileClip
from moviepy.video.fx.all import crop
from syntesize import syntesize
from database import AskReddit, Comment, make_connection, make_session
from settings import GAMEPLAY_FOLDER, AUDIO_FOLDER_ASKREDDIT, SCREENSHOT_FOLDER_ASKREDDIT


def create_video(submission, comments, audio_path: str, video_path: str, screenshot_path: str, width: int, height:  int,):
    audio_path = _create_folder(submission, path=audio_path)
    _synthesize(submission=submission, comments=comments, path=audio_path)
    video_path, video_duration = _get_video_duration(path=video_path)
    audio, total_audio_duration = _get_audio_duration(audio_path)
    clip = _create_subclip(video_path=video_path, video_duration=video_duration, audio_duration=total_audio_duration, width=width, height=height)
    audio_object = _add_sound(audios=audio, path=audio_path)
    screenshot_objects = _add_screenshots(submission=submission, audios=audio, path=screenshot_path, width=width)
    
    new_clip = CompositeVideoClip([clip, *screenshot_objects])
    new_clip = new_clip.set_audio(audio_object)
    new_clip.write_videofile(filename = "test.mp4")


def _add_screenshots(submission, audios, path: str, width:int, start: int = 1):
    path = os.path.join(path, submission.submission_id)
    screenshots = os.listdir(path)
    screenshots = screenshots[::-1]
    audios = audios[::-1]
    screenshot_objects = []
    for screenshot, audio in zip(screenshots, audios):
        duration = audio[1]
        screenshot_objects.append(ImageClip(os.path.join(path, screenshot)).set_start(start).set_duration(duration).set_pos(("center","center")).resize(width=width))
        start+=duration+1
    return screenshot_objects


def _add_sound(audios, path:str, start: int = 1):
    audios = audios[::-1]
    audio_objects = []
    for audio in audios:
        duration = audio[1]
        audio_objects.append(AudioFileClip(os.path.join(path, audio[0])).set_start(start))
        start+=duration+1
    return CompositeAudioClip(audio_objects)


def _create_subclip(video_path: str, video_duration: int,
                    audio_duration: int, width: int, height: int):
    start_time = random.randint(int(audio_duration), int(video_duration))-2*audio_duration
    end_time = start_time+audio_duration
    clip = VideoFileClip(filename=video_path, audio=False)
    size = clip.size
    clip = clip.subclip(start_time, end_time)  # make random part
    clip = crop(clip, x1=(size[0]-width)/2, y1=0,
                x2=(size[0]+width)/2, y2=height)
    return clip


def _get_audio_duration(path: str) -> tuple[list[str, int], list[str, int],]:
    # get names of mp3 files
    audio_names = os.listdir(os.path.join(path))
    # iterate through files get name, duration
    audio = tuple([audio_name, AudioFileClip(filename=os.path.join(
        path, audio_name)).duration] for audio_name in audio_names)

    total = 0
    for duration in audio:
        total += duration[1]

    return audio, total


def _get_video_duration(path: str) -> tuple[str, int]:
    # get all video in the folder
    all_videos = os.listdir(os.path.join(path))
    # randomly choose one video
    video = random.choice(all_videos)
    # get path of the video
    video_path = os.path.join(path, video)
    duration = VideoFileClip(filename=video_path).duration
    return video_path, duration


def _synthesize(submission, comments, path: str) -> str:
    syntesize(text=submission.title, path=path,
              filename=f"title_{submission.submission_id}.mp3")
    print("Title syntesized")

    for comment in comments:
        syntesize(text=comment.content, path=path,
                  filename=f"comment_{comment.comment_id}")
        print("comment")


def _create_folder(submission, path: str):
    new_folder = os.path.join(path, submission.submission_id)
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    return new_folder

if __name__ == "__main__":
    engine = make_connection()
    session = make_session(engine)
    submission = AskReddit.get_submission(session, "10opflg")
    comments = Comment.get_comments(session, submission.submission_id)

    create_video(submission=submission, comments=comments, audio_path=AUDIO_FOLDER_ASKREDDIT, video_path=GAMEPLAY_FOLDER, screenshot_path=SCREENSHOT_FOLDER_ASKREDDIT, width=480, height=854)
