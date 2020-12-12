#!/usr/bin/env python
from dataclasses import dataclass
from typing import List
from data.sql import execute, fetch_one, fetch_all


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

    def find_by_part_of_name(self, part_of_name: str) -> List[Employee]:
        parts = list(filter(lambda x: x.strip() != "", part_of_name.split(" ")))
        parts = list(map(lambda x: "{0}%".format(x), parts))
        if len(parts) == 0:
            return []
        query = " and ".join(map(lambda x: "UPPER(name) LIKE UPPER(?)", parts))
        rows = fetch_all("SELECT employee_id, name, birthday FROM employees WHERE {0}".format(query), *parts)
        return list(map(self.__row_to_entity, rows))

    def find_all(self) -> List[Employee]:
        rows = fetch_all("SELECT employee_id, name, birthday FROM employees ORDER BY employee_id")
        return list(map(self.__row_to_entity, rows))
    
    def __row_to_entity(self, row):
        if row == None:
            return None
        return Employee(row[1], row[2], row[0])
