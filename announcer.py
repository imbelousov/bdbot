#!/usr/bin/env python
import time
from data.employees import EmployeeRepo
from data.scheduled_birthdays import ScheduledBirthdayRepo
from threading import Thread
from dates import *


class Announcer():
    """
    Отвечает за рассылку различных уведомлений
    """

    __PRELIMINARY_BD_ANNOUNCE_DAYS = 2

    def start(self):
        thread = Thread(target=self.__main_loop)
        thread.setDaemon(True)
        thread.setName("Announcer")
        thread.start()

    def __main_loop(self):
        while True:
            self.__schedule_birthdays()
            time.sleep(5)

    def __schedule_birthdays(self):
        scheduled_birthday_repo = ScheduledBirthdayRepo()
        employee_repo = EmployeeRepo()
        employees = employee_repo.find_all()
        for employee in employees:
            bd = calc_next_birthday(timestamp_to_date(employee.birthday))
            days_to_bd = (bd() - today()).days
            bd_timestamp = date_to_timestamp(bd)
            if days_to_bd <= self.__PRELIMINARY_BD_ANNOUNCE_DAYS and scheduled_birthday_repo.is_scheduled(employee.id, bd_timestamp, days_to_bd):
                scheduled_birthday_repo.schedule(employee.id, bd_timestamp, days_to_bd)
