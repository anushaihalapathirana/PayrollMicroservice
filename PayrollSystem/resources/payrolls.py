"""
    This resource file contains the payroll related REST calls implementation
"""
import json
import datetime
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
        daysToWork = 20
        allowedLeaves = 1

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            req = request.json
            employeeList = req["items"]
            today = datetime.date.today()
            margin = datetime.timedelta(days=20)
            df = today-margin

            body = {}
            body['payroll'] = []

            for employee in employeeList:
                data = {}
                monthlyLeaves = []
                salary = 0
                empID = employee["emp"]["employee_id"]
                accNo = employee["emp"]["account_number"]
                basicSalary = employee['emp']['basic_salary']
                oneDaySalary = basicSalary/daysToWork

                leaves = employee['leaves']
                for leave in leaves:
                    leaveDate = datetime.datetime.strptime(
                        leave['leave_date'], "%Y-%m-%dT%H:%M:%S")
                    print("TYPE", type(leaveDate.date()))

                    if(df <= leaveDate.date()):
                        monthlyLeaves.append(leave)

                if(len(monthlyLeaves) > allowedLeaves):
                    salary = basicSalary - \
                        (oneDaySalary * (len(monthlyLeaves) - allowedLeaves))
                else:
                    salary = basicSalary

                data['salary'] = salary
                data['basic'] = basicSalary
                data['deducted'] = basicSalary - salary
                data['accNo'] = accNo
                data['empID'] = empID
                data['payrollDate'] = str(today.isoformat())
                # data['payrollDate'] = json.dumps(datetime.datetime.combine(today, datetime.time(0, 0)), indent = 4, sort_keys = True, default = str)
                data['payrollStartDate'] = str(df.isoformat())
                body['payroll'].append(data)

        except Exception as error:
            print(error)
            return create_error_message(
                500, "Error occurred",
                "payroll Calculation Error")

        return Response(json.dumps(body), status=200, mimetype="application/json")
