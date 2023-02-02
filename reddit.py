import json
import os
import praw
from prawcore.exceptions import ResponseException
from playwright.sync_api import sync_playwright
from settings import CLIENT_ID, CLIENT_SECRET, USER_AGENT
from settings import TRUEOFFMYCHEST, ASKREDDIT
from settings import SCREENSHOT_FOLDER_ASKREDDIT, SCREENSHOT_FOLDER_TRUEOFFMYCHEST
from exceptions import CantLoginReddit
from typing import NewType

reddit: NewType = praw.Reddit

class Reddit:

    reddit_object = None
    cookies = None

    def __init__(self, client_id, client_secret, user_agent) -> None:
        if Reddit.reddit_object is None:
            Reddit.reddit_object = self._login(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        if Reddit.cookies is None:
            Reddit.cookies = self._get_cookies("cookies.json")
        self.submissions = None

    def _login(self, client_id, client_secret, user_agent) -> reddit:
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
    def get_submissions(self, subreddit: str, limit: int = 5) -> list:
        # TODO: Check whether post already in database
        self.submissions = list(self.reddit_object.subreddit(subreddit).top(time_filter = "day", limit=limit))

    @staticmethod
    def get_submission_id(submission):
        return submission.id

    @staticmethod
    def get_title(submission):
        return submission.title

    @staticmethod
    def get_content(submission):
        return submission.selftext
    
    @staticmethod
    def get_comments(submission, limit: int = 10) -> list:
        # self.submission = self.reddit_object.submission(id=submission_id)
        submission.comment_limit = limit
        submission.comment_sort = "best"
        submission.comments.replace_more(limit = 0)
        comments = submission.comments
        return comments
    
    @classmethod
    def get_screenshot_title(cls, submission, path: str):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                locale="en-us",
                color_scheme="dark",
            )
            context.add_cookies(cls.cookies)
            
            page = context.new_page()

            new_folder = os.path.join(path, submission.id)
            if not os.path.exists(new_folder):
                os.mkdir(os.path.join(path, submission.id))
            if page.locator('[data-testid="content-gate"]').is_visible():
            # This means the post is NSFW and requires to click the proceed button.
                page.locator('[data-testid="content-gate"] button').click()
                page.wait_for_load_state()  # Wait for page to fully load
            if page.locator('[data-click-id="text"] button').is_visible():
                page.locator(
                    '[data-click-id="text"] button'
                ).click()  # Remove "Click to see nsfw" Button in Screenshot

            print(submission.permalink)
            page.goto(f"https://www.reddit.com{submission.permalink}")
            page.locator('[data-test-id="post-content"]').screenshot(path=os.path.join(new_folder, f"title_{submission.id}.png"))

            browser.close()

    @classmethod
    def get_screenshot_comments(cls, submission, comments: list, path: str):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                locale="en-us",
                color_scheme="dark",
            )
            context.add_cookies(cls.cookies)
            
            page = context.new_page()

            new_folder = os.path.join(path, submission.id)
            if not os.path.exists(new_folder):
                os.mkdir(os.path.join(path, submission.id))

            for comment in comments:
                print(comment.permalink)
                page.goto(f"https://www.reddit.com{comment.permalink}")
                page.locator(f"#t1_{comment.id}").screenshot(path=os.path.join(new_folder, f"comment_{comment.id}.png"))

            browser.close()
    
    @classmethod
    def _get_cookies(cls, file: str):
        with open(file, "r") as cookie_file:
            cookies = json.load(cookie_file)
        return cookies