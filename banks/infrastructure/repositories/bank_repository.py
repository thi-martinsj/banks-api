import logging

from sqlalchemy.exc import IntegrityError

from banks import db
from banks.domain.entities import Bank
from banks.domain.exceptions import (
    BankAlreadyExistsException,
    BankException
)
from banks.domain.repositories import BankRepository
from ..models import Bank as BankModel


logger = logging.getLogger("banks-api")


class PostgresBankRepository(BankRepository):
    @classmethod
    def add(cls, bank: Bank) -> Bank:
        logger.info(
            "Inserting a new bank into database.",
            extra={
                "props": {
                    "name": bank.name,
                    "ispb": bank.ispb
                }
            }
        )

        try:
            bank_model = BankModel(
                name=bank.name,
                ispb=bank.ispb
            )
            db.session.add(bank_model)
            db.session.commit()
        except IntegrityError as e:
            logger.error(
                "Bank already exists in database.",
                extra={
                    "props": {
                        "name": bank.name,
                        "ispb": bank.ispb,
                        "exception": str(e)
                    }
                }
            )
            raise BankAlreadyExistsException
        except Exception as e:
            logger.error(
                "Error inserting bank into database.",
                extra={
                    "props": {
                        "name": bank.name,
                        "ispb": bank.ispb,
                        "exception": str(e)
                    }
                }
            )
            raise BankException

        logger.info(
            "Bank inserted successfully.",
            extra={
                "props": {
                    "id": str(bank_model.id),
                    "name": bank_model.name,
                    "ispb": bank_model.ispb
                }
            }
        )

        bank.id = bank_model.id

        return bank
