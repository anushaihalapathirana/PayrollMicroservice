"""
    This resource file contains the payroll related REST calls implementation
"""
from jsonschema import validate, ValidationError
from flask import Response, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from PayrollSystem import db
from PayrollSystem.models import Payroll
from PayrollSystem.utils import create_error_message

class PayrollCollection(Resource):
    """ This class contains the GET and POST method implementations for payroll data
        Arguments:
        Returns:
        Endpoint: /api/payrolls/
    """
    def get(self):
        """ GET list of payrolls
            Arguments:
            Returns:
                List of payrolls
            responses:
                '200':
                description: The Payrolls retrieve successfully
        """
        response_data = []
        payrolls = Payroll.query.all()

        for payroll in payrolls:
            response_data.append(payroll.serialize())
        return response_data

    def post(self):
        """ Create a new Payroll
        Arguments:
            request:
                date: 2002-20-1
                amount: 12356
                employee_id: 001
        Returns:
            responses:
                '201':
                description: The Payroll was created successfully
                '400':
                description: The request body was not valid
                '409':
                description: A payroll with the same code already exists
                '415':
                description: Wrong media type was used
        """
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Payroll.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            payroll = Payroll()
            payroll.deserialize(request)
            db.session.add(payroll)
            db.session.commit()
        except Exception as error:
            if isinstance(error, HTTPException):
                return create_error_message(
                     409, "Already Exist",
                    "payroll code is already exist"
            )
        return Response(response={}, status=201)

# class PayrollItem(Resource):
#     """ This class contains the GET, PUT and DELETE method implementations for a single payroll
#         Arguments:
#         Returns:
#         Endpoint - /api/payrolls/<payroll>
#     """
#     def get(self, payroll):
#         """ get details of one payroll
#         Arguments:
#             payroll
#         Returns:
#             Response
#                 '200':
#                 description: Data of list of payroll
#                 '404':
#                 description: The payroll was not found
#         """
#         response_data =  payroll.serialize()

#         return response_data

#     def delete(self, payroll):
#         """ Delete the selected payroll
#         Arguments:
#             payroll
#         Returns:
#             responses:
#                 '204':
#                     description: The payroll was successfully deleted
#                 '404':
#                     description: The payroll was not found
#         """
#         db.session.delete(payroll)
#         db.session.commit()

#         return Response(status=204)

#     def put(self, payroll):
#         """ Replace payroll's basic data with new values
#         Arguments:
#             payroll
#         Returns:
#             responses:
#                 '204':
#                 description: The payroll's attributes were updated successfully
#                 '400':
#                 description: The request body was not valid
#                 '404':
#                 description: The payroll was not found
#                 '409':
#                 description: A payroll with the same name already exists
#                 '415':
#                 description: Wrong media type was used
#         """
#         db_payroll = Payroll.query.filter_by(code=payroll.id).first()

#         if not request.json:
#             return create_error_message(
#                 415, "Unsupported media type",
#                 "Payload format is in an unsupported format"
#             )

#         try:
#             validate(request.json, Payroll.get_schema())
#         except ValidationError:
#             return create_error_message(
#                 400, "Invalid JSON document",
#                 "JSON format is not valid"
#             )

#         db_payroll.name = request.json["name"]
#         db_payroll.id = request.json["code"]
#         db_payroll.description = request.json["description"]

#         try:
#             db.session.commit()
#         except Exception: return create_error_message(
#                 500, "Internal server Error",
#                 "Error while updating the payroll"
#             )

#         return Response(status = 204)
