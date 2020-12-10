#!/usr/bin/env python
from dataclasses import dataclass
from data import execute, fetch_one


@dataclass
class Org:
    """
    Модель организатора дней рождений
    """

    id: int
    employee_id: str
    chat_id: int


class OrgRepo:
    """
    Предоставляет доступ к хранилищу организаторов дней рождений
    """

    def find_by_chat_id(self, chat_id: int) -> Org:
        return None
