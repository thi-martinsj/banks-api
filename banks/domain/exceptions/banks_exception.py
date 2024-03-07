from enum import Enum

from .common import (
    GenericException,
    IntegrityErrorException
)


class BankErrorCodes(Enum):
    BANK1000 = "Bank error. Please try again later. If the problem persists, please contact the support team."
    BANK1001 = "Bank already exists."


class BankException(GenericException):
    code = BankErrorCodes.BANK1000.name
    message = BankErrorCodes.BANK1000.value


class BankAlreadyExistsException(IntegrityErrorException):
    code = BankErrorCodes.BANK1001.name
    message = BankErrorCodes.BANK1001.value
