from unittest.mock import Mock

import pytest

from banks.domain.repositories import BankRepository


def test_add_should_raise_not_implemented_error():
    with pytest.raises(NotImplementedError):
        BankRepository.add(Mock())


def test_list_should_raise_not_implemented_error():
    with pytest.raises(NotImplementedError):
        BankRepository.list()


def test_get_should_raise_not_implemented_error():
    with pytest.raises(NotImplementedError):
        BankRepository.get(Mock())


def test_update_should_raise_not_implemented_error():
    with pytest.raises(NotImplementedError):
        BankRepository.update(Mock())


def test_delete_should_raise_not_implemented_error():
    with pytest.raises(NotImplementedError):
        BankRepository.delete(Mock())
