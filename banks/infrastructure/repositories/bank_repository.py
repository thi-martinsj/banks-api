import logging
from uuid import UUID

from sqlalchemy import (
    delete,
    update
)
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
                    "bank": repr(bank)
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
            db.session.rollback()
            logger.error(
                "Bank already exists in database.",
                extra={
                    "props": {
                        "bank": repr(bank),
                        "exception": str(e)
                    }
                }
            )
            raise BankAlreadyExistsException
        except Exception as e:
            db.session.rollback()
            logger.error(
                "Error inserting bank into database.",
                extra={
                    "props": {
                        "bank": repr(bank),
                        "exception": str(e)
                    }
                }
            )
            raise BankException

        bank.id = bank_model.id

        logger.info(
            "Bank inserted successfully.",
            extra={
                "props": {
                    "bank": repr(bank)
                }
            }
        )

        return bank

    @classmethod
    def get(cls, bank_id: UUID) -> Bank:
        logger.info(
            "Retrieving bank from database.",
            extra={
                "props": {
                    "id": str(bank_id)
                }
            }
        )

        try:
            bank = db.session.query(BankModel).get(str(bank_id))
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

    @classmethod
    def update(cls, bank: Bank) -> Bank:
        logger.info(
            "Updating bank in database.",
            extra={
                "props": {
                    "bank": repr(bank)
                }
            }
        )

        try:
            db.session.execute(
                update(BankModel),
                [
                    bank.dict
                ]
            )
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logger.error(
                "Error updating bank in database.",
                extra={
                    "props": {
                        "bank": repr(bank),
                        "exception": str(e)
                    }
                }
            )

            raise BankException

        logger.info(
            "Updated bank in database successfully.",
            extra={
                "props": {
                    "bank": repr(bank)
                }
            }
        )

        return bank

    @classmethod
    def delete(cls, bank_id: UUID) -> None:
        logger.info(
            "Deleting bank from database.",
            extra={
                "props": {
                    "bank_id": bank_id
                }
            }
        )

        try:
            db.session.execute(
                delete(BankModel)
                .where(
                    BankModel.id == str(bank_id)
                )
            )
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(
                "Error deleting bank from database.",
                extra={
                    "props": {
                        "bank_id": bank_id,
                        "exception": str(e)
                    }
                }
            )
            raise BankException

        logger.info(
            "Bank deleted from database successfully.",
            extra={
                "props": {
                    "bank_id": bank_id
                }
            }
        )
