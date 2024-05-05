import logging

from typing import Optional

from banks.domain.entities import Bank
from banks.domain.exceptions import (
    BankAlreadyExistsException,
    BankException,
    BankNotFoundException
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

    @classmethod
    def get_banks(cls, filters: Optional[dict], bank_repository: BankRepository) -> Bank:
        authorized_filters = ["offset", "limit", "ispb", "name"]
        filters = {k: v for k, v in filters.items() if k in authorized_filters}

        logger.info(
            "Retrieving banks.",
            extra={
                "props": {
                    "filters": filters
                }
            }
        )

        try:
            banks = bank_repository.list(**filters)
        except BankException as e:
            logger.error(
                "Error retrieving banks.",
                extra={
                    "props": {
                        "filters": filters
                    }
                }
            )
            raise e

        if not banks:
            logger.info(
                "Banks not found.",
                extra={
                    "props": {
                        "filters": filters
                    }
                }
            )
            raise BankNotFoundException

        logger.info(
            "Banks retrieved successfully.",
            extra={
                "props": {
                    "filters": filters
                }
            }
        )

        return {
            "banks": [bank.dict for bank in banks],
            "offset": int(filters.get("offset", 0)),
            "limit": int(filters.get("limit", 50))
        }

    @classmethod
    def get_bank(cls, bank_id: str, bank_repository: BankRepository) -> Bank:
        logger.info(
            "Retrieving bank.",
            extra={
                "props": {
                    "bank_id": str(bank_id)
                }
            }
        )

        try:
            bank = bank_repository.get(bank_id)
        except BankException as e:
            logger.error(
                "Error retrieving bank.",
                extra={
                    "props": {
                        "bank_id": str(bank_id)
                    }
                }
            )
            raise e

        if not bank:
            logger.info(
                "Bank not found.",
                extra={
                    "props": {
                        "bank_id": str(bank_id)
                    }
                }
            )
            raise BankNotFoundException

        logger.info(
            "Bank retrieved successfully.",
            extra={
                "props": {
                    "bank": bank.dict
                }
            }
        )

        return bank

    @classmethod
    def update_bank(
        cls,
        bank_id: str,
        mapping: BankMapping,
        bank_repository: BankRepository
    ) -> Bank:
        logger.info(
            "Updating bank.",
            extra={
                "props": {
                    "bank_id": str(bank_id),
                    "ispb": mapping.ispb,
                    "name": mapping.name
                }
            }
        )

        bank = cls.get_bank(bank_id=bank_id, bank_repository=bank_repository)
        bank.ispb = mapping.ispb
        bank.name = mapping.name

        try:
            bank_repository.update(bank)
        except BankException as e:
            logger.error(
                "Error updating bank.",
                extra={
                    "props": {
                        "bank_id": str(bank_id),
                        "ispb": mapping.ispb,
                        "name": mapping.name
                    }
                }
            )
            raise e

        logger.info(
            "Bank updated successfully.",
            extra={
                "props": {
                    "bank_id": str(bank_id),
                    "ispb": mapping.ispb,
                    "name": mapping.name
                }
            }
        )

        return bank
