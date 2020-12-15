#!/usr/bin/env python
from data.sql import execute, fetch_one


class ScheduledBirthdayRepo:
    """
    Предоставляет доступ к отметкам о планировании рассылок по дням рождениям
    """

    def is_scheduled(self, employee_id: int, date: int, preliminary: int) -> bool:
        row = fetch_one("SELECT * FROM scheduled_birthdays WHERE employee_id = ? AND date = ? AND preliminary = ?", employee_id, date, preliminary)
        return row != None

    def schedule(self, employee_id: int, date: int, preliminary: int):
        execute("INSERT INTO scheduled_birthdays (employee_id, date, preliminary) VALUES (?, ?, ?)", employee_id, date, preliminary)
