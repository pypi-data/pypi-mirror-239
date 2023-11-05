class ValidationError(Exception):
    def __init__(self,  message="Failed validation"):
        self.message = message
        super().__init__(self.message)
