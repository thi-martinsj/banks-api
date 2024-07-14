from unittest.mock import patch

import pytest

from banks import db
from banks.domain.exceptions import (
    BankAlreadyExistsException,
    BankException
)


def test_add_should_add_a_bank_into_database_when_bank_does_not_exist_in_database(bank, app):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    bank_response = PostgresBankRepository.add(bank)

    bank_model = db.session.query(BankModel).get(bank_response.id)

    assert bank_response.id == bank_model.id
    assert bank_response.ispb == bank_model.ispb == bank.ispb
    assert bank_response.name == bank_model.name == bank.name

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 1


def test_add_should_raise_bank_already_exists_exception_when_trying_to_add_the_same_bank(bank, app):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    bank_response = PostgresBankRepository.add(bank)

    bank_model = db.session.query(BankModel).get(bank_response.id)

    assert bank_response.id == bank_model.id
    assert bank_response.ispb == bank_model.ispb == bank.ispb
    assert bank_response.name == bank_model.name == bank.name

    with pytest.raises(BankAlreadyExistsException):
        PostgresBankRepository.add(bank)

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 1


@patch.object(db.session, "add")
def test_add_should_raise_bank_exception_when_some_unknown_error_is_raised(add_mock, bank, app):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    add_mock.side_effect = Exception("Oh nooo!")

    with pytest.raises(BankException):
        PostgresBankRepository.add(bank)

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 0
