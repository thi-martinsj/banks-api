import pytest
from uuid import UUID

from banks.domain.entities import Bank
from banks.interface.mappings import BankMapping


@pytest.fixture
def bank_payload():
    return {
        "ispb": "001",
        "name": "Bank of Brazil"
    }


@pytest.fixture
def bank_mapping(bank_payload):
    return BankMapping(payload=bank_payload)


@pytest.fixture
def bank_list():
    return [
        Bank(
            id=UUID("4f98e65f-2adc-400f-8d61-c9e02382c7b3"),
            name="Bank Test 01",
            ispb="100"
        ),
        Bank(
            id=UUID("25eff335-658e-4093-8a11-390e1bff053b"),
            name="Bank Test 02",
            ispb="200"
        ),
        Bank(
            id=UUID("31df7675-51c8-4d6c-a305-cdc7bf816ed3"),
            name="Bank Test 03",
            ispb="300"
        )
    ]
