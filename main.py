from syntesize import syntesize
from reddit import login, get_submissions, get_comments, get_content
from settings import CLIENT_ID, CLIENT_SECRET, USER_AGENT, ASKREDDIT, TRUEOFFMYCHEST
from database import make_connection, make_session, add_submission_TrueOffMyHeart

def add_TrueOffMyHeart(reddit, session):
    submission = get_submissions(reddit, TRUEOFFMYCHEST, 1)
    id = submission[0].id
    title = submission[0].title
    content = get_content(reddit, id)
    print(id)
    print(title)
    print(content[:100])
    add_submission_TrueOffMyHeart(session = session, submission_id = id, title = title, content = content)


def main():
    reddit = login(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)
    connection = make_connection()
    session = make_session(connection)
    # submission = get_submissions(reddit, ASKREDDIT, 1)
    # comment = get_comments(reddit, submission[0].id, limit=1)
    
    add_TrueOffMyHeart(reddit, session)
    
    # syntesize(comment[0].body, filename='test')

if __name__ == "__main__":
    main()