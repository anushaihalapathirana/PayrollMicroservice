
"""
This file contains the Converter methods
"""
from werkzeug.routing import BaseConverter
from payroll_system.models import Payroll
from payroll_system.utils import create_error_message

class PayrollConverter(BaseConverter):
    """
    Converter for Payroll entity in URL parameter
    """
    def to_python(self, value):
        """
        convert to a payroll object
        """
        payroll = Payroll.query.filter_by(code=value).first()
        if payroll is None:
            return create_error_message(
                404, "Not found",
                "Payroll not found"
            )
        return payroll

    def to_url(self, value):
        """
        return payroll code
        """
        return str(value.code)
