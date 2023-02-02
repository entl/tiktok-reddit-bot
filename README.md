# TikTok Reddit bot

This bot was created to make TikTok videos from posts on Reddit. By default there 2 subreddits which used by this bot: ***TrueOffMyChest*** and ***askReddit***. There 2 ways of obtaining content, for instance, in subreddit TrueOffMyChest, I did not found useful to get comments, unlike, in askReddit.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
git clone https://github.com/entl/tiktok-reddit-bot.git
cd tiktok-reddit-bot
pip install -r requirements.txt
```

## Usage

```python
python main.py
```

## Known bugs and possible improvements
1. Not implemented creating video from subreddit TrueOffMyChest 
2. Sometimes NSFW posts return an error
3. If link is in submission, synthesize pronounce it
4. No user input validation (in process)
5. "final_video.py" needs refactoring (in process)
6. To decrease number of arguements in functions they should be grouped (in process)
7. Create meaningful comments (in process)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
Copyright (c) [2023] [Maksym Vorobyov]
