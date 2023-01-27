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

class RecordNotExists(Exception):
    def __init__(self):
        self.message = 'There is no record with provided submission_id'
    
    def __str__(self) -> str:
        return self.message