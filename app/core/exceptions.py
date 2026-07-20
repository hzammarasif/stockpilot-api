class StockPilotException(Exception):
    status_code: int = 500
    detail: str = "Internal server error."


class EmailAlreadyExistsException(StockPilotException):
    status_code = 409
    detail = "Email already exists."


class InvalidCredentialsException(StockPilotException):
    status_code = 401
    detail = "Invalid email or password."


class UserNotFoundException(StockPilotException):
    status_code = 404
    detail = "User not found."

class UnauthorizedException(StockPilotException):
    status_code = 401
    detail = "Unauthorized." 