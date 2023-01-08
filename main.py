from syntesize import syntesize
from reddit import login, get_posts, get_comments
from settings import CLIENT_ID, CLIENT_SECRET, USER_AGENT, SUBREDDIT

def main():
    login_obj = login(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)
    posts = get_posts(login_obj, SUBREDDIT, 1)
    comment = get_comments(login_obj, posts[0].id, limit=1)
    syntesize(comment[0].body, filename='test')

if __name__ == "__main__":
    main()