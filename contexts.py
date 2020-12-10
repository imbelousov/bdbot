#!/usr/bin/env python
from dataclasses import dataclass
from employees import Employee


@dataclass
class AddEmployeeContext:

    employee: Employee = Employee(None, None)
    has_name: bool = False


@dataclass
class AuthContext:

    employee_id: int = 0
    found_employee: bool = False
