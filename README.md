# PWP SPRING 2021
# Human Resource Management System
# Group information

* Student 1. Anusha Ihalapathirana - aihalapa20@student.oulu.fi
* Student 2. Sameera Wickramasekara - spandith21@student.oulu.fi

# Setup database
 - Requirements : Python3, Pip

- Libraries used : flask, flask_sqlalchemy, requests

Please install all the dependencies using
```  
    pip install -r requirements.txt
```
# Setup database

Our system contains with 2 databases. HR Core database and Payroll database. This repository contains the Payroll Microservice

Follow below instructions to setup the databases

***Note*** : _the sqlite db files are already present in the project (hrcodedb and payrolldb). Please delete them first to run these scripts_


1. run payrolldb_data_script.py file using below command. it will generate the payroll database and insert data to the table.

```
    python payrolldb_data_script.py
```

More details about the database can be found here - https://github.com/anushaihalapathirana/PWP/wiki/Database-design-and-implementation

# Run Payroll microservice

Use below commands to run payroll microservice

```
    export FLASK_APP=payroll_system/
    flask run --port=5500
```

Application will run on http://127.0.0.1:5500/ 

# Code quality

Pylint use to check code quality in this project

```
pylint payroll_system/
```