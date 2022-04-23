"""
This file contains the mapping of api resources
"""
from flask import Blueprint
from flask_restful import Api
from PayrollSystem.resources.payrolls import PayrollCollection

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

# related resources
api.add_resource(PayrollCollection, "/payrolls/")
