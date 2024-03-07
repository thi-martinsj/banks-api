from http import HTTPStatus

from flask_restx import (
    Namespace,
    Resource
)

from .api import api
from .schemas import (
    create_bank_request_model,
    create_bank_response_model,
    forbidden_response_model,
    general_error_response_model,
    unauthorized_response_model
)
from banks.application.services import BankService
from banks.interface.decorators import expect_json_data
from banks.interface.mappings import BankMapping


ns = Namespace(
    name="Banks",
    description="Endpoint to manage banks",
    path="/v1/banks"
)
ns.add_model(create_bank_request_model.name, create_bank_request_model)
ns.add_model(create_bank_response_model.name, create_bank_response_model)
ns.add_model(forbidden_response_model.name, forbidden_response_model)
ns.add_model(general_error_response_model.name, general_error_response_model)
ns.add_model(unauthorized_response_model.name, unauthorized_response_model)

api.add_namespace(ns)


def get_repository():
    from banks.infrastructure.repositories import PostgresBankRepository
    return PostgresBankRepository


@ns.route("")
@ns.response(HTTPStatus.BAD_REQUEST, "Unexpected error", general_error_response_model)
@ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized", unauthorized_response_model)
@ns.response(HTTPStatus.FORBIDDEN, "Forbidden", forbidden_response_model)
class Banks(Resource):
    @expect_json_data(ns, BankMapping, create_bank_request_model)
    @ns.response(HTTPStatus.CREATED, "Bank created successfully", create_bank_response_model)
    def post(self, mapping: BankMapping) -> tuple[dict, HTTPStatus]:
        bank = BankService.create_bank(mapping, get_repository())
        return bank.dict, HTTPStatus.CREATED
