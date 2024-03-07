from flask_restx import fields, Model

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
