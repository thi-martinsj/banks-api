from http import HTTPStatus

from flask import request
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
    general_not_found_response_model,
    get_banks_params,
    get_banks_response_model,
    unauthorized_response_model
)
from banks.application.services import BankService
from banks.interface.decorators import expect_json_data
from banks.interface.mappings import BankMapping


ns = Namespace(
    name="Banks",
    description="Endpoints to manage banks",
    path="/v1/banks"
)
ns.add_model(create_bank_request_model.name, create_bank_request_model)
ns.add_model(create_bank_response_model.name, create_bank_response_model)
ns.add_model(forbidden_response_model.name, forbidden_response_model)
ns.add_model(general_error_response_model.name, general_error_response_model)
ns.add_model(general_not_found_response_model.name, general_not_found_response_model)
ns.add_model(get_banks_response_model.name, get_banks_response_model)
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

    @ns.response(HTTPStatus.OK, "Banks retrieved successfully", get_banks_response_model)
    @ns.response(HTTPStatus.NOT_FOUND, "Resource not found", general_not_found_response_model)
    @ns.expect(get_banks_params, validate=True)
    def get(self) -> tuple[dict, HTTPStatus]:
        banks = BankService.get_banks(request.args, get_repository())
        return banks, HTTPStatus.OK


@ns.route("/<uuid:bank_id>")
@ns.response(HTTPStatus.BAD_REQUEST, "Unexpected error", general_error_response_model)
@ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized", unauthorized_response_model)
@ns.response(HTTPStatus.FORBIDDEN, "Forbidden", forbidden_response_model)
class Bank(Resource):
    @ns.response(HTTPStatus.OK, "Bank retrieved successfully", create_bank_response_model)
    @ns.response(HTTPStatus.NOT_FOUND, "Resource not found", general_not_found_response_model)
    def get(self, bank_id: str) -> tuple[dict, HTTPStatus]:
        bank = BankService.get_bank(bank_id, get_repository())
        return bank.dict, HTTPStatus.OK

