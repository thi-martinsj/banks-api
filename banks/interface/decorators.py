from functools import wraps

from flask import request
from flask_restx import (
    Model,
    Namespace
)

from .mappings import BaseMapping


def expect_json_data(ns: Namespace, mapping: BaseMapping, model: Model):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            mapping_instance = mapping(request.json)
            return f(mapping=mapping_instance, *args, **kwargs)

        return ns.expect(model, validate=True)(wrapper)
    return decorator
