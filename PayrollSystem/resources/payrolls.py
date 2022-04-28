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
        """ Create Payroll data. auxilary service.
        Arguments:
            request:
        Returns:
            responses:
                '500':
                description: internal error
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
            margin = datetime.timedelta(days = 20)

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
                    leaveDate = datetime.datetime.strptime(leave['leave_date'], "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d')
                    df = datetime.datetime.combine(today-margin, datetime.time(0, 0))
                    
                    if(df <= datetime.datetime.strptime(leaveDate, "%Y-%m-%d")):
                        monthlyLeaves.append(leave)
              
                if(len(monthlyLeaves) > allowedLeaves):
                    salary = basicSalary - (oneDaySalary * (len(monthlyLeaves) - allowedLeaves))
                else:
                    salary = basicSalary

                data['salary'] = salary
                data['basic'] = basicSalary
                data['deducted'] = basicSalary - salary
                data['accNo'] = accNo
                data['empID'] = empID
                data['payrollDate'] = json.dumps(datetime.datetime.combine(today, datetime.time(0, 0)), indent = 4, sort_keys = True, default = str)
                data['payrollStartDate'] = json.dumps(datetime.datetime.combine(today, datetime.time(0, 0)), indent = 4, sort_keys = True, default = str)
                body['payroll'].append(data)

        except Exception as error:
            return create_error_message(
                     500, "Error occurred",
                    "payroll Calculation Error")
            
        return Response(json.dumps(body), status=200, mimetype="application/json")

