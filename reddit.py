import praw
from prawcore.exceptions import ResponseException
from settings import CLIENT_ID, CLIENT_SECRET, USER_AGENT
from settings import TRUEOFFMYCHEST, ASKREDDIT
from exceptions import CantLoginReddit
from typing import TypeAlias

reddit: TypeAlias = praw.Reddit


def login(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT) -> reddit:
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    try:
        # used to verify whether login is successfull
        list(reddit.subreddit('test').hot(limit=1))[0]
        return reddit
    except ResponseException as e:
        raise CantLoginReddit

# TODO: Implement fetching next submission in the subreddit use the subreddit.new()
# get last most popular subreddits based on limit
def get_submissions(reddit: reddit, subreddit: str, limit: int = 1) -> list:
    # TODO: Check whether post already in database
    return list(reddit.subreddit(subreddit).hot(limit=limit))


def get_comments(reddit: reddit, submission_id: str, limit: int = 10) -> list:
    submission = reddit.submission(id=submission_id)
    submission.comment_limit = limit
    submission.comments.replace_more(limit=0)
    submission.comment_sort = "top"
    comments = submission.comments.list()
    return comments

# get text of the submission usualy is used for subreddit "TrueOffMyChest"
def get_content(reddit: reddit, submission_id: str):
    submission = reddit.submission(id=submission_id)
    return submission.selftext


def main():
    reddit = login()
    comments = []
    for submission in get_submissions(reddit=reddit, subreddit=ASKREDDIT, limit=1):
        print("Title: " + submission.title)
        for comment in get_comments(reddit=reddit, submission_id=submission.id, limit=3):
            comments.append({"submission_id": submission.id, "author": comment.author.name, "content": comment.body})
            # comment.body
            # print("------------")
            # print(comment.author)
            # print(comment.body)
    print(comments)
    # for submission in get_submissions(reddit=reddit, subreddit=TRUEOFFMYCHEST, limit=2):
    #     print("Title: " + submission.title)
    #     print(get_content(reddit=reddit, submission_id=submission.id)[:100])


if __name__ == "__main__":
    main()
