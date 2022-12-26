import praw
from praw.models import MoreComments
from settings import CLIENT_ID, CLIENT_SECRET, USER_AGENT, SUBREDDIT
from exceptions import CantLoginReddit

def login():
    reddit = praw.Reddit(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        user_agent = USER_AGENT,
    )

    if reddit.read_only == False:
        raise CantLoginReddit
    return reddit

def get_posts(reddit: praw.Reddit, subreddit:str):
    # TODO: Check whether post already in database
    return reddit.subreddit(subreddit).hot(limit=1)


if __name__ == "__main__":
    reddit_obj = login()
    # for post in get_posts(reddit=reddit_obj, subreddit=SUBREDDIT):
    #     print(post.title)
    print(get_posts(reddit=reddit_obj, subreddit=SUBREDDIT))

# url = "https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"
# submission = reddit.submission(url=url)

# for top_level_comment in submission.comments:
#     if isinstance(top_level_comment, MoreComments):
#         continue
#     print(top_level_comment.body)