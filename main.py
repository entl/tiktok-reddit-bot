from art import tprint
from reddit import Reddit
from gameplay import download_gameplay
from final_video import create_video
from database import TrueOffMyChest, AskReddit, Comment, make_connection, make_session
from settings import CLIENT_ID, CLIENT_SECRET, USER_AGENT, ASKREDDIT, TRUEOFFMYCHEST
from settings import DATABASE_USER, DATABASE_PWD, DATABASE_LOCATION, DATABASE_NAME
from settings import WIDTH, HEIGHT, AUDIO_FOLDER_ASKREDDIT, GAMEPLAY_FOLDER, VIDEO_FOLDER_ASKREDDIT, SCREENSHOT_FOLDER_ASKREDDIT


def _database_connection():
    engine = make_connection(user=DATABASE_USER, pwd=DATABASE_PWD,
                             location=DATABASE_LOCATION, name=DATABASE_NAME)
    session = make_session(engine=engine)
    return engine, session


def get_posts_menu():
    print("1. AskReddit\n2. TrueOffMyChest(Not available)\n3. Back")
    user_choice = input("Choose subreddit: ")
    quantity_submissions = int(input("How many posts do you want to get?"))
    quantity_comments = int(
        input("How many comments from post do you want to get?"))
    if user_choice == "1":
        _get_from_askreddit(
            limit_submissions=quantity_submissions, limit_comments=quantity_comments)
    elif user_choice == "2":
        _get_from_trueoffmychest()
    else:
        return


def _get_submissions(session):
    return AskReddit.get_not_uploaded_submission(session=session)


def _get_from_askreddit(limit_submissions, limit_comments):
    reddit = Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET, user_agent=USER_AGENT)
    print(reddit)
    reddit.get_submissions(subreddit=ASKREDDIT, limit=limit_submissions)
    for submission in reddit.submissions:
        reddit.get_screenshot_title(submission=submission, path=SCREENSHOT_FOLDER_ASKREDDIT)
        comments = reddit.get_comments(
            submission=submission, limit=limit_comments)
        reddit.get_screenshot_comments(submission=submission, comments=comments, path=SCREENSHOT_FOLDER_ASKREDDIT)
        _add_askreddit(submission=submission, comments=comments)
    print("Success")


def _get_from_trueoffmychest():
    print("In development...")


def _add_askreddit(submission, comments):
    engine, session = _database_connection()
    AskReddit.add_submission(session=session, submission_id=submission.id,
                             author=submission.author.name, title=submission.title)
    format_comments = Comment.format_comments(comments=comments)
    Comment.add_comments(session=session, comments=format_comments)


def create_video_menu():
    engine, session = _database_connection()
    submissions = _get_submissions(session)
    print("What post would you like to upload?")
    for i, submission in enumerate(submissions, start=1):
        print(f"{i}. {submission.title}")

    while True:
        user_choice = int(input("Choose post: "))
        if user_choice <= len(submissions):
            submission = submissions[user_choice-1]
            comments = Comment.get_comments(
                session=session, submission_id=submission.submission_id)
            _create_video(submission=submission, comments=comments)
            AskReddit.set_uploaded(session=session, submission_id=submission.submission_id)
            break
        print("Enter correct number")


def _create_video(submission, comments):
    create_video(submission=submission, comments=comments, audio_path=AUDIO_FOLDER_ASKREDDIT, gameplay_path=GAMEPLAY_FOLDER,
                 save_path=VIDEO_FOLDER_ASKREDDIT, screenshot_path=SCREENSHOT_FOLDER_ASKREDDIT, width=WIDTH, height=HEIGHT)


def download_video_from_youtube():
    link = input("Enter link to the video on Youtube: ")
    download_gameplay(link=link)


def fetch_records_menu():
    engine, session = _database_connection()
    records = AskReddit.get_all_submissions(session=session)
    for record in records:
        print(f"- {record.title}")


def menu():
    while True:
        initial_menu = """1. Get posts from Reddit \n2. Create video\n3. Download video from Youtube\n4. Get submissions\n5. Exit"""
        print(initial_menu)
        user_choice = input("Choose one: ")

        if user_choice == "1":
            get_posts_menu()
        elif user_choice == "2":
            create_video_menu()
        elif user_choice == "3":
            download_video_from_youtube()
        elif user_choice == "4":
            fetch_records_menu()
        else:
            exit(0)


def main():
    tprint("TikTok Reddit Bot")
    menu()


if __name__ == "__main__":
    main()
