from enum import Enum


class ErrorCodes(Enum):
    BANK9000 = "Unexpected error. Please try again later. If the problem persists, please contact the support team."
    BANK9001 = "Invalid token. Check if the token is in header or if it is valid and try again."
    BANK9003 = "User is not authorized to do this action."


class GenericException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class ForbiddenException(Exception):
    pass


class IntegrityErrorException(Exception):
    pass
