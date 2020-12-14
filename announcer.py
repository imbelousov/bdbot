#!/usr/bin/env python
import time
from data.employees import EmployeeRepo
from threading import Thread


class Announcer():
    """
    Отвечает за рассылку различных уведомлений
    """

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
        employee_repo = EmployeeRepo()
