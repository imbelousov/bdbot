#!/usr/bin/env python
from dataclasses import dataclass
from typing import List
from data import execute, fetch_one, fetch_all


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
        return self.__row_to_entity(row)

    def find_by_name(self, name: str) -> Employee:
        row = fetch_one("SELECT employee_id, name, birthday FROM employees WHERE name = ?", name)
        return self.__row_to_entity(row)

    def find_all(self) -> List[Employee]:
        list = []
        rows = fetch_all("SELECT employee_id, name, birthday FROM employees ORDER BY name")
        for row in rows:
            list.append(self.__row_to_entity(row))
        return list
    
    def __row_to_entity(self, row):
        if row == None:
            return None
        return Employee(row[1], row[2], row[0])
