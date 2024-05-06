import logging
from http import HTTPStatus
from jwt import InvalidSignatureError

from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restx import Api

from banks.domain.exceptions import (
    ErrorCodes,
    ForbiddenException,
    GenericException,
    IntegrityErrorException,
    NotFoundException
)


logger = logging.getLogger("banks-api")


def register_error_handlers(api: Api):
    @api.errorhandler(InvalidSignatureError)
    @api.errorhandler(NoAuthorizationError)
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

    @api.errorhandler(IntegrityErrorException)
    def handle_integrity_error(error) -> tuple[dict, HTTPStatus]:
        return {
            "code": error.code,
            "message": error.message
        }, HTTPStatus.BAD_REQUEST

    @api.errorhandler(NotFoundException)
    def handle_not_found_error(error) -> tuple[dict, HTTPStatus]:
        return {
            "code": error.code,
            "message": error.message
        }, HTTPStatus.NOT_FOUND

    @api.errorhandler(GenericException)
    def handle_generic_exception_error(error) -> tuple[dict, HTTPStatus]:
        return {
            "code": error.code,
            "message": error.message
        }, HTTPStatus.BAD_REQUEST

    @api.errorhandler(Exception)
    def handle_unknown_exception_error(error) -> tuple[dict, HTTPStatus]:
        logger.error(
            "Unexpected error",
            extra={
                "props": {
                    "exception": str(error)
                }
            }
        )
        return {
            "code": ErrorCodes.BANK9000.name,
            "message": ErrorCodes.BANK9000.value
        }, HTTPStatus.BAD_REQUEST
