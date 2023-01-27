class CantLoginReddit(Exception):
    def __init__(self):
        self.message = 'Login is unsuccessful'
    
    def __str__(self) -> str:
        return self.message

class CantAddRecord(Exception):
    def __init__(self):
        self.message = 'Adding record is unsuccessful'
    
    def __str__(self) -> str:
        return self.message