#!/usr/bin/env python
import configparser
from data import init_db, create_tables
from employees import Employee, EmployeeRepo
from orgs import Org, OrgRepo
from dates import *
from secret_codes import *


def main():
    config = configparser.ConfigParser()
    config.read("focus_bd_bot.ini")
    init_db(config["Sqlite"]["FileName"])

    create_tables()

    employee_repo = EmployeeRepo()
    org_repo = OrgRepo()

    print("Введите имя первого организатора дней рождений:")
    name = input()

    print("Введите его дату рождения:")
    birthday = date_to_timestamp(parse_date(input()))

    employee = Employee(name, birthday)
    employee_repo.add(employee)
    org = Org(employee.id, 0, generate_secret_code())
    org_repo.add(org)

    print("Организатор зарегистрирован. Его секретный код: {0}.".format(org.secret_code))

if __name__ == "__main__":
    main()
