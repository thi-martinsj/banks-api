from http import HTTPStatus

from flask_restx import Api

from banks.domain.exceptions import (
    ErrorCodes,
    ForbiddenException,
    UnauthorizedException
)


def register_error_handlers(api: Api):
    @api.errorhandler(UnauthorizedException)
    def handle_unauthorized_error(error) -> tuple[dict, HTTPStatus]:
        return {
            "code": ErrorCodes.BANK9001.name,
            "message": ErrorCodes.BANK9001.value
        }, HTTPStatus.UNAUTHORIZED

    @api.errorhandler(ForbiddenException)
    def handle_forbidden_error(error) -> tuple[dict, HTTPStatus]:
        return {
            "code": ErrorCodes.BANK9003.name,
            "message": ErrorCodes.BANK9003.value
        }, HTTPStatus.FORBIDDEN

    @api.errorhandler(Exception)
    def handle_generic_exception_error(error) -> tuple[dict, HTTPStatus]:
        return {
            "code": ErrorCodes.BANK9000.name,
            "message": ErrorCodes.BANK9000.value
        }, HTTPStatus.BAD_REQUEST
