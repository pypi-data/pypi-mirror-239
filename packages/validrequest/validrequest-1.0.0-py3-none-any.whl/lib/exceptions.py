class ValidationError(Exception):
    def __init__(self,  message="Failed validation", error_code=400):
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)
