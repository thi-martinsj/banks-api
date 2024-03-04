from flask_restx import fields, Model


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
