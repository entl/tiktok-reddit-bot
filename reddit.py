import praw
from settings import CLIENT_ID, CLIENT_SECRET, USER_AGENT, SUBREDDIT
from exceptions import CantLoginReddit
from typing import TypeAlias

Login_obj: TypeAlias = praw.Reddit

def login(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, user_agent = USER_AGENT) -> Login_obj:
    login_obj = praw.Reddit(
        client_id = client_id,
        client_secret = client_secret,
        user_agent = user_agent,
    )
    #Raise error if login was unsuccessful
    if login_obj.read_only == False:
        raise CantLoginReddit
    return login_obj

#get last most popular subreddits based on limit
def get_posts(reddit: Login_obj, subreddit:str, limit:int = 1) -> list:
    # TODO: Check whether post already in database
    return list(reddit.subreddit(subreddit).hot(limit=limit))

#get comments from subreddit
def get_comments(reddit: Login_obj, post_id: str, limit:int = 10) -> list:
    submission = reddit.submission(id=post_id)
    #get rid of MoreComments class in submission
    submission.comments.replace_more(limit=0)
    submission.comment_sort = "top"
    #TODO: optimize speed of getting comments
    comments = submission.comments.list()
    return comments[:limit]


if __name__ == "__main__":
    reddit_obj = login()
    # for post in get_posts(reddit=reddit_obj, subreddit=SUBREDDIT):
    #     print(post.title)
    #     for comment in get_comments(reddit=reddit_obj, post_id=post.id):
    #         print("------------")
    #         print(comment.author)
    #         print(comment.body)
    #     print(post.title)
