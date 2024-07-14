import pytest

from banks.domain.entities import Bank


def test_bank_should_set_a_value_for_id_when_defining_a_value_for_id_that_is_not_defined(bank_payload):
    bank = Bank(bank_payload["name"], bank_payload["ispb"])
    bank.id = "c62aa7a7-88a0-4c4d-93bd-fc8a434aedc5"

    assert bank.id is not None


def test_bank_should_raise_value_error_when_defining_a_value_for_id_that_is_alread_defined():
    with pytest.raises(ValueError) as e:
        bank = Bank("Test", "123", "e5b2f499-9bd7-4309-82bd-a0f81c05d414")
        bank.id = "f07cc2b9-b9cf-4105-94eb-e2a1f883a702"

    assert str(e.value) == "ID is already set."
    assert bank.id == "e5b2f499-9bd7-4309-82bd-a0f81c05d414"


def test_bank_should_set_a_name_when_name_is_not_none(bank_payload):
    bank = Bank(bank_payload["name"], bank_payload["ispb"])
    bank.name = "Testing new name"

    assert bank.name == "Testing new name"
    assert bank.name != bank_payload["name"]


def test_bank_should_not_set_a_name_when_name_is_none(bank_payload):
    bank = Bank(bank_payload["name"], bank_payload["ispb"])
    bank.name = None

    assert (bank.name) == bank_payload["name"]


def test_bank_should_set_ispb_when_value_is_not_none(bank_payload):
    bank = Bank(bank_payload["name"], bank_payload["ispb"])
    bank.ispb = "123456789"

    assert bank.ispb == "123456789"
    assert bank.ispb != bank_payload["ispb"]


def test_bank_should_not_set_ispb_when_value_is_none(bank_payload):
    bank = Bank(bank_payload["name"], bank_payload["ispb"])
    bank.ispb = None

    assert (bank.ispb) == bank_payload["ispb"]
