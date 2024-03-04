from flask_restx import Api


VERSION = "1.0.0"
DESCRIPTION = "API do manage banks context"

api = Api(
    title="Banks API",
    version=VERSION,
    description=DESCRIPTION,
    doc="/docs"
)
