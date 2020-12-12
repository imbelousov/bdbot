#!/usr/bin/env python
from dataclasses import dataclass
from data.sql import execute, fetch_one


@dataclass
class Org:
    """
    Модель организатора дней рождений
    """

    employee_id: int
    chat_id: int
    secret_code: str
    org_id: int = 0


class OrgRepo:
    """
    Предоставляет доступ к хранилищу организаторов дней рождений
    """

    def add(self, org: Org):
        org.org_id = execute("INSERT INTO orgs (employee_id, chat_id, secret_code) VALUES (?, ?, ?)", org.employee_id, org.chat_id, org.secret_code)

    def set_chat_id(self, org_id: int, chat_id: int):
        execute("UPDATE orgs SET chat_id = ? WHERE org_id = ?", chat_id, org_id)

    def find_by_chat_id(self, chat_id: int) -> Org:
        row = fetch_one("SELECT org_id, employee_id, chat_id, secret_code FROM orgs WHERE chat_id = ?", chat_id)
        return self.__row_to_entity(row)
    
    def find_by_secret_code(self, secret_code: str) -> Org:
        row = fetch_one("SELECT org_id, employee_id, chat_id, secret_code FROM orgs WHERE secret_code = ?", secret_code)
        return self.__row_to_entity(row)

    def find_by_employee_id(self, employee_id: int) -> Org:
        row = fetch_one("SELECT org_id, employee_id, chat_id, secret_code FROM orgs WHERE employee_id = ?", employee_id)
        return self.__row_to_entity(row)

    def __row_to_entity(self, row):
        if row == None:
            return None
        return Org(row[1], row[2], row[3], row[0])
