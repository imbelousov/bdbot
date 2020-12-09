#!/usr/bin/env python
import sqlite3
from dataclasses import dataclass


@dataclass
class Org:
    """
    Модель организатора дней рождений
    """

    id: int
    name: str
    chat_id: int


class OrgRepo:
    """
    Предоставляет доступ к хранилищу организаторов дней рождений
    """

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.__create_tables()

    def find_by_chat_id(self, chat_id: int) -> Org:
        conn = self.__create_connection()
        c = conn.cursor()
        c.execute("""
            SELECT org_id, name
            FROM orgs
            WHERE chat_id = {0}
        """.format(chat_id))
        row = c.fetchone()
        if row == None:
            return None
        return Org(id=row["org_id"], name=row["name"], chat_id=chat_id)

    def find_by_id(self, id: int) -> Org:
        conn = self.__create_connection()
        c = conn.cursor()
        c.execute("""
            SELECT name, chat_id
            FROM orgs
            WHERE org_id = {0}
        """.format(id))
        row = c.fetchone()
        if row == None:
            return None
        return Org(id=id, name=row["name"], chat_id=row["chat_id"])

    def create(self, chat_id: int) -> int:
        conn = self.__create_connection()
        c = conn.cursor()
        c.execute("""
            INSERT INTO orgs (chat_id)
            VALUES ({0})
        """.format(chat_id))
        return c.lastrowid

    def __create_connection(self):
        return sqlite3.connect(self.file_name)

    def __create_tables(self):
        conn = self.__create_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orgs (
                org_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NULL,
                chat_id INTEGER NULL
            )
        """)
