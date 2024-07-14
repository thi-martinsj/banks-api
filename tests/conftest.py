import os

import pytest
from flask_migrate import upgrade, downgrade
from uuid import UUID

from banks import create_app, db
from banks.domain.entities import Bank
from banks.interface.mappings import BankMapping


@pytest.fixture(scope="session")
def app():
    os.environ["DEPLOY_ENV"] = "Testing"
    _app = create_app()
    _app.app_context().push()

    with _app.app_context():
        upgrade(directory='migrations')

    yield _app

    with _app.app_context():
        downgrade(directory='migrations', revision='base')
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def clean_db(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()


@pytest.fixture
def client(app):
    return app.test_client()


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
def bank(bank_payload):
    return Bank(
        name=bank_payload["name"],
        ispb=bank_payload["ispb"]
    )


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
