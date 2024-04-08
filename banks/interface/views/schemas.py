from flask_restx import (
    fields,
    Model,
    reqparse
)

from banks.domain.exceptions import ErrorCodes


health_response_model = Model(
    "Health Status",
    {
        "service": fields.String(
            description="Service name",
            required=True,
            example="banks-api"
        ),
        "version": fields.String(
            description="Service version",
            required=True,
            example="1.0.0"
        )
    }
)


create_bank_request_model = Model(
    "Create Bank Request",
    {
        "ispb": fields.String(
            description="ISPB code",
            required=True,
            example="001"
        ),
        "name": fields.String(
            description="Bank name",
            required=True,
            example="Bank of Brazil"
        )
    }
)


create_bank_response_model = create_bank_request_model.clone(
    "Create Bank Response",
    {
        "id": fields.Integer(
            description="Bank id",
            required=True,
            example="510af4d3-1c6a-419f-b344-388c8c4d854e"
        )
    }
)


get_banks_response_model = Model(
    "Get Banks Response",
    {
        "banks": fields.List(
            fields.Nested(create_bank_response_model),
            description="List of banks",
            required=True
        ),
        "offset": fields.Integer(
            description="Offset for pagination",
            required=True,
            example=0
        ),
        "limit": fields.Integer(
            description="Limit for pagination",
            required=True,
            example=50
        )
    }
)


get_banks_params = reqparse.RequestParser()
get_banks_params.add_argument(
    "name",
    type=str,
    required=False,
    help="Bank name"
)
get_banks_params.add_argument(
    "ispb",
    type=str,
    required=False,
    help="ISPB code"
)
get_banks_params.add_argument(
    "offset",
    type=int,
    required=False,
    default=0,
    help="Offset for pagination"
)
get_banks_params.add_argument(
    "limit",
    type=int,
    required=False,
    default=50,
    help="Limit for pagination"
)


general_error_response_model = Model(
    "General Error",
    {
        "code": fields.String(
            description="Error code",
            required=True,
            example=ErrorCodes.BANK9000.name
        ),
        "message": fields.String(
            description="Error message",
            required=True,
            example=ErrorCodes.BANK9000.value
        )
    }
)


unauthorized_response_model = Model(
    "Unauthorized Error",
    {
        "code": fields.String(
            description="Unauthorized code",
            required=True,
            example=ErrorCodes.BANK9001.name
        ),
        "message": fields.String(
            description="Unauthorized error message",
            required=True,
            example=ErrorCodes.BANK9001.value
        )
    }
)


forbidden_response_model = Model(
    "Forbidden Error",
    {
        "code": fields.String(
            description="Forbidden error code",
            required=True,
            example=ErrorCodes.BANK9003.name
        ),
        "message": fields.String(
            description="Forbidden error message",
            required=True,
            example=ErrorCodes.BANK9003.value
        )
    }
)


general_not_found_response_model = Model(
    "Not Found",
    {
        "code": fields.String(
            description="Not found code",
            required=True,
            example=ErrorCodes.BANK9004.name
        ),
        "message": fields.String(
            description="Not found message",
            required=True,
            example=ErrorCodes.BANK9004.value
        )
    }
)



