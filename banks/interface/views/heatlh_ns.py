from flask_restx import Namespace, Resource

from .api import api, VERSION
from .schemas import health_response_model


ns = Namespace(
    name="Health Status",
    description="Endpoint to check application health",
    path="/health"
)
ns.add_model(health_response_model.name, health_response_model)

api.add_namespace(ns)


@ns.route("")
class Health(Resource):
    @ns.response(code=200, description="Health Status Success", model=health_response_model)
    def get(self) -> dict:
        return {
            "service": "banks-api",
            "version": VERSION
        }
