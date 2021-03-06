# this script use to enter data to the payroll database
"""
This class use to generate database and its data
"""
from datetime import datetime
import click
from flask.cli import with_appcontext
from payroll_system import db
from payroll_system.models import Payroll

@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Method to initializa database
    """
    print("create database--------------------------------------------")
    db.create_all()


@click.command("testgen")
@with_appcontext
def generate_test_data():
    """
    Method to generate fake data
    """

    payroll = Payroll(date=datetime(2018, 12, 21, 11, 20, 30),
                    amount=125553, employee_id="001")
    payroll2 = Payroll(date=datetime(2018, 11, 21, 11, 20, 30),
                    amount=125553, employee_id="002")
    payroll3 = Payroll(date=datetime(2018, 10, 21, 11, 20, 30),
                    amount=125553, employee_id="001")
    payroll4 = Payroll(date=datetime(2018, 9, 21, 11, 20, 30),
                    amount=125553, employee_id="002")
    payroll5 = Payroll(date=datetime(2018, 12, 21, 11, 20, 30),
                    amount=125553, employee_id="003")
    payroll6 = Payroll(date=datetime(2018, 11, 21, 11, 20, 30),
                    amount=125553, employee_id="002")
    payroll7 = Payroll(date=datetime(2018, 12, 21, 11, 20, 30),
                    amount=125553, employee_id="003")
    payroll8 = Payroll(date=datetime(2018, 12, 21, 11, 20, 30),
                    amount=125553, employee_id="001")

    db.session.add(payroll, payroll2, payroll3,
    payroll4, payroll5,
    payroll6, payroll7, payroll8)

    db.session.commit()
