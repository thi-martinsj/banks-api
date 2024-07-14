from unittest.mock import patch

import pytest

from banks import db
from banks.domain.exceptions import (
    BankErrorCodes,
    ErrorCodes
)


BASE_ENDPOINT = "/v1/banks"


def create_headers(token: str):
    return {
        "Authorization": f"Bearer {token}"
    }


def test_post_should_return_401_when_client_is_not_authorized(client, bank_payload):
    response = client.post(BASE_ENDPOINT, json=bank_payload)

    assert response.status_code == 401
    assert response.json == {
        "code": ErrorCodes.BANK9001.name,
        "message": ErrorCodes.BANK9001.value
    }


def test_post_should_return_400_when_there_is_no_payload(client, jwt_token):
    response = client.post(BASE_ENDPOINT, headers=create_headers(jwt_token))

    assert response.status_code == 400
    assert response.json == {
        "code": ErrorCodes.BANK9000.name,
        "message": ErrorCodes.BANK9000.value
    }


def test_post_should_return_400_when_payload_is_invalid(client, jwt_token):
    response = client.post(BASE_ENDPOINT, headers=create_headers(jwt_token), json={})

    assert response.status_code == 400
    assert response.json == {
        "errors": {
            "ispb": "'ispb' is a required property",
            "name": "'name' is a required property"
        },
        "message": "Input payload validation failed"
    }


def test_post_should_return_201_when_bank_is_inserted_into_database_successfully(client, jwt_token, bank_payload):
    from banks.infrastructure.models import Bank as BankModel

    response = client.post(BASE_ENDPOINT, headers=create_headers(jwt_token), json=bank_payload)

    assert response.status_code == 201
    assert response.json["ispb"] == bank_payload["ispb"]
    assert response.json["name"] == bank_payload["name"]

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 1


def test_post_should_return_400_when_bank_already_exists_into_database(client, jwt_token, bank_payload):
    from banks.infrastructure.models import Bank as BankModel

    headers = create_headers(jwt_token)

    response = client.post(BASE_ENDPOINT, headers=headers, json=bank_payload)

    assert response.status_code == 201
    assert response.json["ispb"] == bank_payload["ispb"]
    assert response.json["name"] == bank_payload["name"]

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 1

    response = client.post(BASE_ENDPOINT, headers=headers, json=bank_payload)

    assert response.status_code == 400
    assert response.json == {
        "code": BankErrorCodes.BANK1001.name,
        "message": BankErrorCodes.BANK1001.value
    }

    amount_banks = db.session.query(BankModel).count()

    assert amount_banks == 1


def test_get_all_banks_should_return_401_when_client_is_not_authorized(client):
    response = client.get(BASE_ENDPOINT)

    assert response.status_code == 401
    assert response.json == {
        "code": ErrorCodes.BANK9001.name,
        "message": ErrorCodes.BANK9001.value
    }


@pytest.mark.parametrize(
    "filters, expected_banks_amount",
    [
        ({}, 3),
        ({"ispb": "1"}, 1),
        ({"name": "test_0"}, 1),
        ({"ispb": "2", "name": "test_2"}, 1)
    ]
)
def test_get_all_banks_should_return_200_and_banks_when_there_are_banks_into_database(
    filters,
    expected_banks_amount,
    client,
    jwt_token
):
    headers = create_headers(jwt_token)

    for i in range(3):
        payload = {
            "ispb": f"{i}",
            "name": f"test_{i}"
        }
        client.post(BASE_ENDPOINT, headers=headers, json=payload)

    response = client.get(BASE_ENDPOINT, headers=headers, query_string=filters)

    assert response.status_code == 200
    assert len(response.json["banks"]) == expected_banks_amount


def test_get_all_banks_should_return_404_when_banks_are_not_found(client, jwt_token):
    response = client.get(BASE_ENDPOINT, headers=create_headers(jwt_token))

    assert response.status_code == 404
    assert response.json == {
        "code": BankErrorCodes.BANK1004.name,
        "message": (f"{BankErrorCodes.BANK1004.value} You have requested this URI [/v1/banks] "
                    "but did you mean /v1/banks or /v1/banks/<uuid:bank_id> ?")
    }


@patch.object(db.Query, "filter_by")
def test_get_all_banks_should_return_400_when_some_unknown_error_is_raised(
    filter_by_mock,
    client,
    jwt_token
):
    filter_by_mock.side_effect = Exception("Error :(")

    response = client.get(BASE_ENDPOINT, headers=create_headers(jwt_token))

    assert response.status_code == 400
    assert response.json == {
        "code": BankErrorCodes.BANK1000.name,
        "message": BankErrorCodes.BANK1000.value
    }


def test_get_a_bank_should_return_401_when_client_is_not_authorized(client):
    response = client.get(f"{BASE_ENDPOINT}/c7bd4b58-092a-4a45-8aa3-c26cae73a1d7")

    assert response.status_code == 401
    assert response.json == {
        "code": ErrorCodes.BANK9001.name,
        "message": ErrorCodes.BANK9001.value
    }


def test_get_a_bank_should_return_200_when_bank_exists_in_database(client, jwt_token, bank_payload):
    headers = create_headers(jwt_token)

    response_post = client.post(BASE_ENDPOINT, headers=headers, json=bank_payload)

    response = client.get(f"{BASE_ENDPOINT}/{response_post.json["id"]}", headers=headers)

    assert response.status_code == 200
    assert response.json == {
        "id": response_post.json["id"],
        "ispb": bank_payload["ispb"],
        "name": bank_payload["name"]
    }


def test_get_a_bank_should_return_404_when_bank_is_not_found_in_database(client, jwt_token):
    response = client.get(f"{BASE_ENDPOINT}/a320f24e-cb0b-417d-ba9d-f21dc637527e", headers=create_headers(jwt_token))

    assert response.status_code == 404
    assert response.json == {
        "code": BankErrorCodes.BANK1004.name,
        "message": BankErrorCodes.BANK1004.value
    }


def test_patch_should_return_401_when_client_is_not_authorized(client, bank_payload):
    response = client.patch(f"{BASE_ENDPOINT}/f94ef55d-11b9-4f13-bcbf-f13623182949", json=bank_payload)

    assert response.status_code == 401
    assert response.json == {
        "code": ErrorCodes.BANK9001.name,
        "message": ErrorCodes.BANK9001.value
    }


def test_patch_should_return_400_when_there_is_no_payload(client):
    response = client.patch(f"{BASE_ENDPOINT}/f94ef55d-11b9-4f13-bcbf-f13623182949")

    assert response.status_code == 400
    assert response.json == {
        "code": ErrorCodes.BANK9000.name,
        "message": ErrorCodes.BANK9000.value
    }


def test_patch_should_return_404_when_bank_does_not_exist_in_database(client, jwt_token):
    response = client.patch(
        f"{BASE_ENDPOINT}/f94ef55d-11b9-4f13-bcbf-f13623182949",
        json={},
        headers=create_headers(jwt_token)
    )

    assert response.status_code == 404
    assert response.json == {
        "code": BankErrorCodes.BANK1004.name,
        "message": BankErrorCodes.BANK1004.value
    }


def test_patch_should_return_200_when_bank_is_updated_successfully(client, bank_payload, jwt_token):
    headers = create_headers(jwt_token)

    post_response = client.post(BASE_ENDPOINT, headers=headers, json=bank_payload)

    response = client.patch(
        f"{BASE_ENDPOINT}/{post_response.json["id"]}",
        json={
            "ispb": "987654"
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json == {
        "id": post_response.json["id"],
        "ispb": "987654",
        "name": bank_payload["name"]
    }

    get_response = client.get(f"{BASE_ENDPOINT}/{post_response.json["id"]}", headers=headers)

    assert response.json == get_response.json


def test_delete_should_return_401_when_client_is_not_authorized(client):
    response = client.delete(f"{BASE_ENDPOINT}/7d4c60cb-1054-4d7f-a720-930ea51e1903")

    assert response.status_code == 401
    assert response.json == {
        "code": ErrorCodes.BANK9001.name,
        "message": ErrorCodes.BANK9001.value
    }


def test_delete_should_return_404_when_bank_does_not_exist_in_database(client, jwt_token):
    response = client.delete(
        f"{BASE_ENDPOINT}/5a0e7cca-b3ec-4613-bb43-47be950b5aa9",
        headers=create_headers(jwt_token)
    )

    assert response.status_code == 404
    assert response.json == {
        "code": BankErrorCodes.BANK1004.name,
        "message": BankErrorCodes.BANK1004.value
    }


def test_delete_should_return_200_when_bank_is_deleted_from_database_successfully(client, jwt_token, bank_payload):
    headers = create_headers(jwt_token)

    post_response = client.post(BASE_ENDPOINT, headers=headers, json=bank_payload)

    get_response = client.get(f"{BASE_ENDPOINT}/{post_response.json["id"]}", headers=headers)

    assert get_response.status_code == 200

    response = client.delete(
        f"{BASE_ENDPOINT}/{post_response.json["id"]}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json == {
        "id": post_response.json["id"],
        "ispb": bank_payload["ispb"],
        "name": bank_payload["name"]
    }

    get_response = client.get(f"{BASE_ENDPOINT}/{post_response.json["id"]}", headers=headers)

    assert get_response.status_code == 404
