#!/usr/bin/env python
from dataclasses import dataclass
from typing import List
from data.sql import execute, fetch_one, fetch_all


@dataclass
class Org:
    """
    Модель организатора дней рождений
    """

    employee_id: int
    chat_id: int
    secret_code: str
    role: int
    org_id: int = 0


class Role:
    """
    Роль организатора дней рождений
    """

    USER = 0
    ADMIN = 10


class OrgRepo:
    """
    Предоставляет доступ к хранилищу организаторов дней рождений
    """

    def add(self, org: Org):
        org.org_id = execute("INSERT INTO orgs (employee_id, chat_id, secret_code, role) VALUES (?, ?, ?, ?)", org.employee_id, org.chat_id, org.secret_code, org.role)

    def set_chat_id(self, org_id: int, chat_id: int):
        execute("UPDATE orgs SET chat_id = ? WHERE org_id = ?", chat_id, org_id)

    def find_by_chat_id(self, chat_id: int) -> Org:
        row = fetch_one("SELECT org_id, employee_id, chat_id, secret_code, role FROM orgs WHERE chat_id = ?", chat_id)
        return self.__row_to_entity(row)
    
    def find_by_secret_code(self, secret_code: str) -> Org:
        row = fetch_one("SELECT org_id, employee_id, chat_id, secret_code, role FROM orgs WHERE secret_code = ?", secret_code)
        return self.__row_to_entity(row)

    def find_by_employee_id(self, employee_id: int) -> Org:
        row = fetch_one("SELECT org_id, employee_id, chat_id, secret_code, role FROM orgs WHERE employee_id = ?", employee_id)
        return self.__row_to_entity(row)

    def find_all(self) -> List[Org]:
        rows = fetch_all("SELECT org_id, employee_id, chat_id, secret_code, role FROM orgs ORDER BY org_id")
        return list(map(self.__row_to_entity, rows))

    def __row_to_entity(self, row):
        if row == None:
            return None
        return Org(row[1], row[2], row[3], row[4], row[0])
