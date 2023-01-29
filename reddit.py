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


# get most popular subreddits in given time period up to limit
def get_submissions(reddit: reddit, subreddit: str, limit: int = 1) -> list:
    # TODO: Check whether post already in database
    return reddit.subreddit(subreddit).top(time_filter = "day", limit=limit)


def get_comments(reddit: reddit, submission_id: str, limit: int = 10) -> list:
    submission = reddit.submission(id=submission_id)
    submission.comment_limit = limit
    submission.comment_sort = "best"
    submission.comments.replace_more(limit = 0)
    comments = submission.comments
    return comments


# get text of the submission usualy is used for subreddit "TrueOffMyChest"
def get_content(reddit: reddit, submission_id: str):
    submission = reddit.submission(id=submission_id)
    return submission.selftext
