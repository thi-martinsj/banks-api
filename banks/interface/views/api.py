from flask_restx import Api


VERSION = "1.0.0"
DESCRIPTION = "API do manage banks context"

api = Api(
    title="Banks API",
    version=VERSION,
    description=DESCRIPTION,
    doc="/docs",
    authorizations={
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Example: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0N"
        }
    }
)
