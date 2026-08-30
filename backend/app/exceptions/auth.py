class InvalidCredentialsException(Exception):

    def __init__(self):

        self.message = "Invalid email or password."

        super().__init__(self.message)


class UnauthorizedException(Exception):

    def __init__(self):

        self.message = "Authentication required."

        super().__init__(self.message)