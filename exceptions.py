class CantLoginReddit(Exception):
    def __init__(self, message):
        self.message = f'Login is unsuccessful. Error: {message}'
    
    def __str__(self) -> str:
        return self.message

class CantAddRecord(Exception):
    def __init__(self, message):
        self.message = f'Adding record is unsuccessful. Error: {message}'
    
    def __str__(self) -> str:
        return self.message

class CantUpdateRecord(Exception):
    def __init__(self, message):
        self.message = f'Updating record is unsuccessful. Error: {message}'
    
    def __str__(self) -> str:
        return self.message


class RecordNotExists(Exception):
    def __init__(self, message):
        self.message = f'There is no record with provided submission_id. Error: {message}'
    
    def __str__(self) -> str:
        return self.message