#!/usr/bin/env python
from dataclasses import dataclass
from data import execute, fetch_one


@dataclass
class Employee:
    """
    Модель сотрудника Фокуса
    """

    name: str
    birthday: int
    id: int = 0


class EmployeeRepo:
    """
    Предоставляет доступ к хранилищу сотрудников
    """

    def add(self, employee: Employee):
        employee.id = execute("INSERT INTO employees (name, birthday) VALUES (?, ?)", employee.name, employee.birthday)

    def find_by_id(self, id: int) -> Employee:
        row = fetch_one("SELECT employee_id, name, birthday FROM employees WHERE employee_id = ?", id)
        if row == None:
            return None
        return Employee(row[1], row[2], row[0])

    def find_by_name(self, name: str) -> Employee:
        row = fetch_one("SELECT employee_id, name, birthday FROM employees WHERE name = ?", name)
        if row == None:
            return None
        return Employee(row[1], row[2], row[0])
