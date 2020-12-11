#!/usr/bin/env python
from dataclasses import dataclass
from employees import Employee


@dataclass
class AddEmployeeContext:

    employee: Employee = Employee(None, None)
    has_name: bool = False


@dataclass
class AddOrgContext:

    pass

@dataclass
class AuthContext:

    pass
