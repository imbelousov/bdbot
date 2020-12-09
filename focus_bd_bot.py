#!/usr/bin/env python
import configparser
import telebot
import time
import datetime
from employees import Employee, EmployeeRepo
from orgs import Org, OrgRepo
from data import init_db


config = configparser.ConfigParser()
config.read("focus_bd_bot.ini")
bot = telebot.TeleBot(config["Api"]["Token"])
init_db(config["Sqlite"]["FileName"])
contexts = {}


def now() -> datetime.date:
    return timestamp_to_date(time.time())


def clear_context(message):
    if message.chat.id in contexts:
        del contexts[message.chat.id]


def is_proper_context(message, expectedType) -> bool:
    return message.chat.id in contexts and type(contexts[message.chat.id]) == expectedType


def timestamp_to_date(ts: int) -> datetime.date:
    return datetime.date.fromtimestamp(ts)


def date_to_timestamp(dt: datetime.date) -> int:
    return time.mktime(dt.timetuple())


def calc_next_birthday(employee: Employee) -> datetime.date:
    dt = timestamp_to_date(employee.birthday)
    while dt < now():
        dt = datetime.date(dt.year + 1, dt.month, dt.day)
    return dt


@bot.message_handler(commands=["cancel"])
def cancel(message):
    """
    Команда /cancel сбрасывает текущий контекст
    """

    clear_context(message)


@bot.message_handler(commands=["add"])
def add_employee(message):
    """
    Команда /add добавляет нового сотрудника Фокуса в базу
    """

    clear_context(message)

    # Шаг 1: Запрос имени сотрудника
    contexts[message.chat.id] = Employee(None, None)
    bot.send_message(message.chat.id, "Как зовут нового сотрудника?")


@bot.message_handler(func=lambda message: is_proper_context(message, Employee))
def continue_add_employee(message):
    """
    Продолжение работы команды /add
    """

    employee = contexts[message.chat.id]
    employee_repo = EmployeeRepo()

    # Шаг 2: Сохранение имени сотрудника и запрос даты рождения
    if employee.name == None:
        if str.isspace(message.text):
            bot.send_message(message.chat.id, "Это не имя. Напиши ещё раз.")
            return
        another_employee = employee_repo.find_by_name(message.text)
        if another_employee != None:
            bot.send_message(message.chat.id, "Такой сотрудник уже есть в базе. Его идентификатор {0}.".format(another_employee.id))
            clear_context(message)
            return
        employee.name = message.text
        bot.send_message(message.chat.id, "А когда он родился? Формат даты: DD.MM.YYYY.")
    
    # Шаг 3: Сохранение даты рождения сотрудника и запись в БД
    else:
        try:
            employee.birthday = time.mktime(datetime.datetime.strptime(message.text, "%d.%m.%Y").timetuple())
        except:
            bot.send_message(message.chat.id, "Я не смог прочитать эту дату. Напиши ещё раз.")
            return
        employee_repo.add(employee)
        bot.send_message(message.chat.id, "Сотрудник {0} сохранён в базе! Его идентификатор {1}.".format(employee.name, employee.id))
        clear_context(message)


@bot.message_handler(commands=["list"])
def add_employee(message):
    """
    Команда /list выводит список всех зарегистрированных сотрудников
    """

    clear_context(message)
    employee_repo = EmployeeRepo()
    employees = employee_repo.find_all()
    bot.send_message(message.chat.id, "\n".join(map(lambda x: "{0}\t{1}\t\tСледующий ДР: {2}".format(x.id, x.name, calc_next_birthday(x)), employees)))


@bot.message_handler(commands=["birthdays"])
def add_employee(message):
    """
    Команда /birthdays выводит список ближайших дней рождений
    """

    clear_context(message)
    employee_repo = EmployeeRepo()
    employees = employee_repo.find_all()
    employees = list(map(lambda x: (x, calc_next_birthday(x)), employees))
    employees = list(map(lambda x: (x[0], x[1], x[1] - now()), employees))
    employees = list(filter(lambda x: x[2].days < 60, employees))
    employees.sort(key=lambda x: x[1])
    if len(employees) > 0:
        bot.send_message(message.chat.id, "\n".join(map(lambda x: "{0} - {1} (осталось {2} дней)".format(x[0].name, x[1], x[2].days), employees)))
    else:
        bot.send_message(message.chat.id, "В ближайшее время не ожидается дней рождений")


@bot.message_handler(func=lambda message: True)
def help(message):
    """
    Вызов справки - команда по умолчанию
    """
    
    clear_context(message)
    bot.send_message(message.chat.id, "\n".join([
        "/add - Добавить нового сотрудника",
        "/list - Показать всех сотрудников",
        "/birthdays - Показать ближайшие дни рождения",
        "/cancel - Отмена текущей команды"
    ]))


bot.polling()
