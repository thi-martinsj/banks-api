from unittest.mock import patch, Mock

import pytest

from banks import db
from banks.domain.entities import Bank
from banks.domain.exceptions import (
    BankAlreadyExistsException,
    BankException
)


def test_add_should_add_a_bank_into_database_when_bank_does_not_exist_in_database(bank):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    bank_response = PostgresBankRepository.add(bank)

    bank_model = db.session.query(BankModel).get(bank_response.id)

    assert bank_response.id == bank_model.id
    assert bank_response.ispb == bank_model.ispb == bank.ispb
    assert bank_response.name == bank_model.name == bank.name

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 1


def test_add_should_raise_bank_already_exists_exception_when_trying_to_add_the_same_bank(bank):
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
def test_add_should_raise_bank_exception_when_some_unknown_error_is_raised(add_mock, bank):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    add_mock.side_effect = Exception("Oh nooo!")

    with pytest.raises(BankException):
        PostgresBankRepository.add(bank)

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 0


def test_get_should_return_a_bank_when_there_is_bank_in_database(bank_list):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    for bank in bank_list:
        bank._id = None
        PostgresBankRepository.add(bank)

    bank = PostgresBankRepository.get(bank_list[1].id)
    amount_banks = db.session.query(BankModel).count()

    assert bank.id is not None
    assert bank.ispb == bank_list[1].ispb
    assert bank.name == bank_list[1].name
    assert amount_banks == 3


def test_get_should_return_none_when_bank_is_not_found_in_database(bank):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    PostgresBankRepository.add(bank)

    bank = PostgresBankRepository.get("32d2bda1-4b07-4906-b97e-ee95d89ae17d")

    amount_banks = db.session.query(BankModel).count()

    assert bank is None
    assert amount_banks == 1


@patch.object(db.Query, "get")
def test_get_should_raise_bank_exception_when_some_unknown_error_is_raised(get_mock):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    get_mock.side_effect = Exception("Error again :(")

    with pytest.raises(BankException):
        PostgresBankRepository.get("90b1e503-f63d-48ad-81da-4e7fc475c01a")

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 0


def test_list_should_return_a_maximum_fifty_banks_when_there_is_neither_filter_nor_limit():
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    for i in range(60):
        PostgresBankRepository.add(Bank(
            name=f"test_{i}",
            ispb=f"{i}"
        ))

    banks = PostgresBankRepository.list()

    assert len(banks) == 50

    for i in range(50):
        assert banks[i].name == f"test_{i}"
        assert banks[i].ispb == f"{i}"

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 60


@pytest.mark.parametrize(
    "filters, expected_amount",
    [
        ({"offset": 0, "limit": 10, "kwargs": {}}, 10),
        ({"offset": 1, "limit": 20, "kwargs": {}}, 20),
        ({"offset": 0, "limit": 3, "kwargs": {"name": "test_1"}}, 1),
        ({"offset": 0, "limit": 50, "kwargs": {"ispb": "58"}}, 1)
    ]
)
def test_list_should_return_banks_according_to_filters_when_there_are_filters(
    filters,
    expected_amount
):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    for i in range(60):
        PostgresBankRepository.add(Bank(
            name=f"test_{i}",
            ispb=f"{i}"
        ))

    banks = PostgresBankRepository.list(
        offset=filters["offset"],
        limit=filters["limit"],
        **filters["kwargs"]
    )

    assert len(banks) == expected_amount

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 60


@patch.object(db.Query, "filter_by")
def test_list_should_raise_bank_exception_when_some_unknown_error_is_raised(filter_by_mock):
    from banks.infrastructure.repositories import PostgresBankRepository

    filter_by_mock.side_effect = Exception("Mocked error")

    with pytest.raises(BankException):
        PostgresBankRepository.list()


def test_update_should_return_bank_when_update_successfully(bank):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    PostgresBankRepository.add(bank)

    bank.ispb = "0002"

    bank_result = PostgresBankRepository.update(bank)

    assert bank_result == bank

    banks = db.session.query(BankModel).all()

    assert banks[0].id == bank_result.id
    assert banks[0].ispb == "0002"
    assert banks[0].name == bank_result.name
    assert len(banks) == 1


@patch.object(db.session, "execute")
def test_update_must_raise_bank_exception_when_some_unknown_exception_is_raised(execute_mock):
    from banks.infrastructure.repositories import PostgresBankRepository

    execute_mock.side_effect = Exception

    with pytest.raises(BankException):
        PostgresBankRepository.update(Mock())


def test_delete_should_remove_a_bank_from_database_when_bank_exists_in_database(bank_list):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    for bank in bank_list:
        bank._id = None
        PostgresBankRepository.add(bank)

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 3

    PostgresBankRepository.delete(bank_list[0].id)

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 2


def test_delete_should_not_remove_a_bank_from_database_when_bank_does_not_exist_in_database(bank_list):
    from banks.infrastructure.models import Bank as BankModel
    from banks.infrastructure.repositories import PostgresBankRepository

    for bank in bank_list:
        bank._id = None
        PostgresBankRepository.add(bank)

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 3

    PostgresBankRepository.delete("7e45e9a5-5cd0-42e2-bbd5-87b78884fce1")

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 3


@patch.object(db.session, "execute")
def test_delete_should_raise_bank_exception_when_some_unknown_error_is_raised(execute_mock):
    from banks.infrastructure.repositories import PostgresBankRepository

    execute_mock.side_effect = Exception

    with pytest.raises(BankException):
        PostgresBankRepository.delete(Mock())
