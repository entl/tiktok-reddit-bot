class CantLoginReddit(Exception):
    def __init__(self):
        self.message = 'Login is unsuccessful'
