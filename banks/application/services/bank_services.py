import logging

from banks.domain.entities import Bank
from banks.domain.exceptions import (
    BankAlreadyExistsException,
    BankException
)
from banks.domain.repositories import BankRepository
from banks.interface.mappings import BankMapping


logger = logging.getLogger("banks-api")


class BankService:
    @classmethod
    def create_bank(cls, mapping: BankMapping, bank_repository: BankRepository) -> Bank:
        logger.info(
            "Creating a new bank.",
            extra={
                "props": {
                    "name": mapping.name,
                    "ispb": mapping.ispb
                }
            }
        )

        try:
            bank = Bank(
                name=mapping.name,
                ispb=mapping.ispb
            )
            bank_repository.add(bank)
        except BankAlreadyExistsException as e:
            logger.error(
                "Bank already exists.",
                extra={
                    "props": {
                        "name": mapping.name,
                        "ispb": mapping.ispb
                    }
                }
            )
            raise e
        except BankException as e:
            logger.error(
                "Error creating bank.",
                extra={
                    "props": {
                        "name": mapping.name,
                        "ispb": mapping.ispb
                    }
                }
            )
            raise e

        logger.info(
            "Bank created successfully.",
            extra={
                "props": {
                    "id": bank.id,
                    "name": bank.name,
                    "ispb": bank.ispb
                }
            }
        )

        return bank
