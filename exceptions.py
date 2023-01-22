class CantLoginReddit(Exception):
    def __init__(self):
        self.message = 'Login is unsuccessful'
    
    def __str__(self) -> str:
        return self.message