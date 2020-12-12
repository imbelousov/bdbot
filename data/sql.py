#!/usr/bin/env python
import sqlite3


__file_name: str = None


def init_db(file_name: str):
    global __file_name
    __file_name = file_name


def execute(query: str, *parameters):
    conn = __create_connection()
    c = conn.cursor()
    c.execute(query, parameters)
    conn.commit()
    return c.lastrowid


def fetch_one(query: str, *parameters):
    conn = __create_connection()
    c = conn.cursor()
    c.execute(query, parameters)
    return c.fetchone()


def fetch_all(query: str, *parameters):
    conn = __create_connection()
    c = conn.cursor()
    c.execute(query, parameters)
    return c.fetchall()


def __create_connection():
    global __file_name
    return sqlite3.connect(__file_name)


def create_tables():
    execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birthday INTEGER NOT NULL
        )
    """)
    execute("""
        CREATE TABLE IF NOT EXISTS orgs (
            org_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            chat_id INTEGER NULL,
            secret_code TEXT NOT NULL,
            role INTEGER NOT NULL,
            FOREIGN KEY(employee_id) REFERENCES eployees(employee_id)
        )
    """)
