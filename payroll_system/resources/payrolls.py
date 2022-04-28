"""
    This resource file contains the payroll related REST calls implementation
"""
import json
import datetime
from flask import Response, request
from flask_restful import Resource
from payroll_system.models import Payroll
from payroll_system.utils import create_error_message


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
        days_to_work = 20
        allowed_leaves = 1

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            req = request.json
            employee_list = req["items"]
            today = datetime.date.today()
            margin = datetime.timedelta(days=20)
            payroll_start = today-margin

            body = {}
            body['payroll'] = []

            for employee in employee_list:
                data = {}
                monthly_leaves = []
                salary = 0
                emp_id = employee["emp"]["employee_id"]
                acc_no = employee["emp"]["account_number"]
                basic_salary = employee['emp']['basic_salary']
                one_day_salary = basic_salary/days_to_work

                leaves = employee['leaves']
                for leave in leaves:
                    leave_date = datetime.datetime.strptime(
                        leave['leave_date'], "%Y-%m-%dT%H:%M:%S")
                    print("TYPE", type(leave_date.date()))

                    if payroll_start <= leave_date.date():
                        monthly_leaves.append(leave)

                if len(monthly_leaves) > allowed_leaves:
                    salary = basic_salary - \
                        (one_day_salary * (len(monthly_leaves) - allowed_leaves))
                else:
                    salary = basic_salary

                data['salary'] = salary
                data['basic'] = basic_salary
                data['deducted'] = basic_salary - salary
                data['accNo'] = acc_no
                data['empID'] = emp_id
                data['payrollDate'] = str(today.isoformat())
                data['payrollStartDate'] = str(payroll_start.isoformat())
                body['payroll'].append(data)

        except Exception as error:
            print(error)
            return create_error_message(
                500, "Error occurred",
                "payroll Calculation Error")

        return Response(json.dumps(body), status=200, mimetype="application/json")
