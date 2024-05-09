from unittest.mock import patch
from uuid import uuid4, UUID

import pytest

from banks.application.services import BankService
from banks.domain.entities import Bank
from banks.domain.exceptions import (
    BankAlreadyExistsException,
    BankException,
    BankNotFoundException
)
from banks.domain.repositories import BankRepository


@patch.object(BankRepository, "add")
def test_create_bank_must_return_bank_model_when_bank_is_inserted_into_database(
    add_mock,
    bank_mapping
):
    uuid = uuid4()

    def side_effect_add(bank):
        bank.id = uuid

    add_mock.side_effect = side_effect_add

    bank = BankService.create_bank(bank_mapping, BankRepository)

    assert isinstance(bank, Bank)
    assert bank.id == str(uuid)
    assert bank.ispb == bank_mapping.ispb
    assert bank.name == bank_mapping.name
    add_mock.assert_called_once_with(bank)


@patch.object(BankRepository, "add")
def test_create_bank_must_raise_bank_already_exists_exception_when_bank_is_already_into_database(
    add_mock,
    bank_mapping
):
    add_mock.side_effect = BankAlreadyExistsException

    with pytest.raises(BankAlreadyExistsException) as e:
        BankService.create_bank(bank_mapping, BankRepository)

    assert e.value.code == BankAlreadyExistsException.code
    assert e.value.message == BankAlreadyExistsException.message
    assert add_mock.call_args[0][0].ispb == bank_mapping.ispb
    assert add_mock.call_args[0][0].name == bank_mapping.name


@patch.object(BankRepository, "add")
def test_create_bank_must_raise_bank_exception_when_some_error_occurs_while_inserting_bank(
    add_mock,
    bank_mapping
):
    add_mock.side_effect = BankException

    with pytest.raises(BankException) as e:
        BankService.create_bank(bank_mapping, BankRepository)

    assert e.value.code == BankException.code
    assert e.value.message == BankException.message
    assert add_mock.call_args[0][0].ispb == bank_mapping.ispb
    assert add_mock.call_args[0][0].name == bank_mapping.name


@patch.object(BankRepository, "list")
@pytest.mark.parametrize(
    "filters, expected_len_list_banks",
    [
        ({}, 3),
        ({"limit": 2}, 2),
        ({"offset": 1, "limit": 2}, 1),
        ({"xpto": "foo"}, 3)
    ]
)
def test_get_banks_must_return_a_list_of_banks_when_there_are_some_banks_into_database(
    list_mock,
    filters,
    expected_len_list_banks,
    bank_list
):
    authorized_filters = ["offset", "limit", "ispb", "name"]
    filters_expected = {k: v for k, v in filters.items() if k in authorized_filters}

    list_mock.return_value = bank_list[
        filters.get("offset", 0):filters.get("limit", 3)
    ]

    response = BankService.get_banks(filters, BankRepository)

    assert len(response["banks"]) == expected_len_list_banks
    assert response["offset"] == filters.get("offset", 0)
    assert response["limit"] == filters.get("limit", 50)
    list_mock.assert_called_once_with(**filters_expected)


@patch.object(BankRepository, "list")
def test_get_banks_must_raise_bank_not_found_exception_when_there_is_no_banks_into_database(
    list_mock
):
    list_mock.return_value = []

    with pytest.raises(BankNotFoundException) as e:
        BankService.get_banks({}, BankRepository)

    assert e.value.code == BankNotFoundException.code
    assert e.value.message == BankNotFoundException.message
    list_mock.assert_called_once_with(**{})


@patch.object(BankRepository, "list")
def test_get_banks_must_raise_bank_exception_when_some_exception_is_raised_while_searching_in_database(
    list_mock
):
    list_mock.side_effect = BankException

    with pytest.raises(BankException) as e:
        BankService.get_banks({}, BankRepository)

    assert e.value.code == BankException.code
    assert e.value.message == BankException.message
    list_mock.assert_called_once_with(**{})


@patch.object(BankRepository, "get")
def test_get_bank_must_return_a_bank_model_when_there_is_a_bank_that_matches_the_given_id(
    get_mock,
    bank_list
):
    bank_id = "4f98e65f-2adc-400f-8d61-c9e02382c7b3"
    get_mock.return_value = bank_list[0]

    bank = BankService.get_bank(UUID(bank_id), BankRepository)

    assert isinstance(bank, Bank)
    assert bank.id == bank_id
    get_mock.assert_called_once_with(UUID(bank_id))


@patch.object(BankRepository, "get")
def test_get_bank_must_raise_bank_not_found_exception_when_there_is_no_bank_that_matches_the_given_id(
    get_mock
):
    bank_id = "4de483e4-17b5-4403-bf5a-c457467a22a7"
    get_mock.return_value = None

    with pytest.raises(BankNotFoundException) as e:
        BankService.get_bank(UUID(bank_id), BankRepository)

    assert e.value.code == BankNotFoundException.code
    assert e.value.message == BankNotFoundException.message
    get_mock.assert_called_once_with(UUID(bank_id))


@patch.object(BankRepository, "get")
def test_get_bank_must_raise_bank_exception_when_some_exception_is_raised_while_searching_into_database(
    get_mock
):
    get_mock.side_effect = BankException

    with pytest.raises(BankException) as e:
        BankService.get_bank(None, BankRepository)

    assert e.value.code == BankException.code
    assert e.value.message == BankException.message
    get_mock.assert_called_once_with(None)


@patch.object(BankRepository, "update")
@patch.object(BankService, "get_bank")
def test_update_bank_must_return_an_updated_bank_model_when_bank_is_successfully_updated_in_database(
    get_bank_mock,
    update_mock,
    bank_list,
    bank_mapping
):
    bank_model = bank_list[1]
    get_bank_mock.return_value = bank_model
    update_mock.return_value = None

    bank = BankService.update_bank(bank_model.id, bank_mapping, BankRepository)

    assert bank.id == bank_model.id
    assert bank.ispb == bank_mapping.ispb
    assert bank.name == bank_mapping.name
    get_bank_mock.assert_called_once_with(bank_model.id, BankRepository)
    update_mock.assert_called_once_with(bank)


@pytest.mark.parametrize(
    "exception",
    [
        (BankNotFoundException),
        (BankException)
    ]
)
@patch.object(BankRepository, "update")
@patch.object(BankService, "get_bank")
def test_update_bank_must_raise_an_exception_when_get_bank_raises_this_exception(
    get_bank_mock,
    update_spy,
    exception,
    bank_mapping
):
    get_bank_mock.side_effect = exception

    with pytest.raises(exception) as e:
        BankService.update_bank(None, bank_mapping, BankRepository)

    assert e.value.code == exception.code
    assert e.value.message == exception.message
    get_bank_mock.assert_called_once_with(None, BankRepository)
    update_spy.assert_not_called()


@patch.object(BankRepository, "update")
@patch.object(BankService, "get_bank")
def test_update_bank_must_raise_bank_exception_when_some_error_occurs_while_updating_data_in_database(
    get_bank_mock,
    update_mock,
    bank_list,
    bank_mapping
):
    bank_model = bank_list[2]
    get_bank_mock.return_value = bank_model
    update_mock.side_effect = BankException

    with pytest.raises(BankException) as e:
        BankService.update_bank(bank_model.id, bank_mapping, BankRepository)

    assert e.value.code == BankException.code
    assert e.value.message == BankException.message
    get_bank_mock.assert_called_once_with(bank_model.id, BankRepository)
    update_mock.assert_called_once_with(bank_model)


@patch.object(BankService, "get_bank")
@patch.object(BankRepository, "delete")
def test_delete_bank_must_return_a_bank_when_this_bank_is_successfully_removed_from_database(
    delete_mock,
    get_bank_mock,
    bank_list
):
    bank_model = bank_list[0]
    get_bank_mock.return_value = bank_model
    delete_mock.return_value = None

    bank = BankService.delete_bank(bank_model.id, BankRepository)

    assert bank == bank_model
    get_bank_mock.assert_called_once_with(bank_model.id, BankRepository)
    delete_mock.assert_called_once_with(bank_model.id)


@pytest.mark.parametrize(
    "exception",
    [
        (BankNotFoundException),
        (BankException)
    ]
)
@patch.object(BankService, "get_bank")
@patch.object(BankRepository, "delete")
def test_delete_bank_must_raise_an_exception_when_get_bank_raises_this_exception(
    delete_spy,
    get_bank_mock,
    exception,
    bank_list
):
    bank_model = bank_list[1]
    get_bank_mock.side_effect = exception

    with pytest.raises(exception) as e:
        BankService.delete_bank(bank_model.id, BankRepository)

    assert e.value.code == exception.code
    assert e.value.message == exception.message
    get_bank_mock.assert_called_once_with(bank_model.id, BankRepository)
    delete_spy.assert_not_called()


@patch.object(BankService, "get_bank")
@patch.object(BankRepository, "delete")
def test_delete_bank_must_raise_bank_exception_when_some_error_occurs_while_deleting_bank_from_database(
    delete_mock,
    get_bank_mock,
    bank_list
):
    bank_model = bank_list[2]
    get_bank_mock.return_value = bank_model
    delete_mock.side_effect = BankException

    with pytest.raises(BankException) as e:
        BankService.delete_bank(bank_model.id, BankRepository)

    assert e.value.code == BankException.code
    assert e.value.message == BankException.message
    get_bank_mock.assert_called_once_with(bank_model.id, BankRepository)
    delete_mock.assert_called_once_with(bank_model.id)
