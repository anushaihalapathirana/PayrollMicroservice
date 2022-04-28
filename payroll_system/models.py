"""
Database model class
"""
from datetime import datetime
from payroll_system import db

class Payroll(db.Model):
    """
    payroll database
    Table-payroll
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    employee_id =  db.Column(db.String(256), nullable=False)

    @staticmethod
    def get_schema():
        """
        method to get schema
        """
        schema = {
            "type": "object",
            "required": ["amount", "date", "employee_id"]
        }
        props = schema["properties"] = {}
        props["amount"] = {
            "description": "amount",
            "type": "number"
        }
        props["date"] = {
            "description": "payroll date",
            "type": "string",
            "format": "date-time"
        }
        props["employee_id"] = {
            "description": "employee id",
            "type": "string"
        }
        return schema

    def serialize(self):
        """
        Serialize method
        """
        role = {
            "id": self.id,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "employee_id": self.employee_id
        }
        return role

    def deserialize(self, request):
        """
        Deserialize method
        """
        self.amount = request.json['amount']
        self.date = datetime.fromisoformat(
            request.json['date'])
        self.employee_id = request.json['employee_id']
 