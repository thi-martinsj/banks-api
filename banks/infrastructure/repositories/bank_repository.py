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

    @classmethod
    def get(cls, bank_id: str) -> Bank:
        logger.info(
            "Retrieving bank from database.",
            extra={
                "props": {
                    "id": str(bank_id)
                }
            }
        )

        try:
            bank = db.session.query(BankModel).get(bank_id)
        except Exception as e:
            logger.error(
                "Error retrieving bank from database.",
                extra={
                    "props": {
                        "id": str(bank_id),
                        "exception": str(e)
                    }
                }
            )

            raise BankException

        logger.info(
            "Bank retrieved successfully from database." if bank else "Bank not found in database.",
            extra={
                "props": {
                    "id": str(bank_id)
                }
            }
        )

        return Bank(
            id=bank.id,
            name=bank.name,
            ispb=bank.ispb
        ) if bank else None

    @classmethod
    def list(cls, offset: int = 0, limit: int = 50, **kwargs) -> list[Bank]:
        logger.info(
            "Retrieving banks from database.",
            extra={
                "props": {
                    "filters": kwargs,
                    "offset": offset,
                    "limit": limit
                }
            }
        )

        try:
            banks = db.session.query(BankModel).filter_by(
                **kwargs).offset(offset).limit(limit).all()
        except Exception as e:
            logger.error(
                "Error retrieving banks from database.",
                extra={
                    "props": {
                        "filters": kwargs,
                        "offset": offset,
                        "limit": limit,
                        "exception": str(e)
                    }
                }
            )

            raise BankException

        logger.info(
            "Banks retrieved successfully from database.",
            extra={
                "props": {
                    "filters": kwargs,
                    "offset": offset,
                    "limit": limit,
                    "amount": len(banks)
                }
            }
        )

        return [
            Bank(
                id=bank.id,
                name=bank.name,
                ispb=bank.ispb
            )
            for bank in banks
        ]
