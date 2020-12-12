#!/usr/bin/env python
import configparser
import telebot
import random
import string
from data.sql import init_db
from data.employees import EmployeeRepo
from data.orgs import Org, OrgRepo
from auth import auth_org
from contexts import *
from dates import *


def generate_secret_code() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=48))


def main():
    config = configparser.ConfigParser()
    config.read("focus_bd_bot.ini")
    bot = telebot.TeleBot(config["Api"]["Token"])
    init_db(config["Sqlite"]["FileName"])
    contexts = {}


    def clear_context(message):
        if message.chat.id in contexts:
            del contexts[message.chat.id]


    def is_proper_context(message, expectedType) -> bool:
        return message.chat.id in contexts and type(contexts[message.chat.id]) == expectedType


    @bot.message_handler(commands=["cancel"])
    def cancel(message):
        """
        Команда /cancel сбрасывает текущий контекст
        """

        clear_context(message)


    @bot.message_handler(commands=["auth"])
    def auth(message):
        """
        Команда /auth авторизует текущего пользователя как организатора дней рождений
        """
        
        clear_context(message)
        
        #Шаг 1: Запрос кода
        contexts[message.chat.id] = AuthContext()
        bot.send_message(message.chat.id, "Напиши свой секретный код")


    @bot.message_handler(func=lambda message: is_proper_context(message, AuthContext))
    def continue_auth(message):
        """
        Продолжение работы команды /auth
        """

        clear_context(message)

        #Шаг 2: Поиск организатора с таким кодом
        org_repo = OrgRepo()
        employee_repo = EmployeeRepo()
        org = org_repo.find_by_secret_code(message.text)
        if org == None:
            bot.send_message(message.chat.id, "Я не нашёл организатора с таким кодом.")
            return
        org_repo.set_chat_id(org.org_id, message.chat.id)
        employee = employee_repo.find_by_id(org.employee_id)
        bot.send_message(message.chat.id, "Привет, {0}!".format(employee.name))


    @bot.message_handler(commands=["add"])
    @auth_org(bot)
    def add_employee(message):
        """
        Команда /add добавляет нового сотрудника Фокуса в базу
        """

        clear_context(message)

        # Шаг 1: Запрос имени сотрудника
        contexts[message.chat.id] = AddEmployeeContext()
        bot.send_message(message.chat.id, "Как зовут нового сотрудника?")


    @bot.message_handler(func=lambda message: is_proper_context(message, AddEmployeeContext))
    @auth_org(bot)
    def continue_add_employee(message):
        """
        Продолжение работы команды /add
        """

        context = contexts[message.chat.id]
        employee_repo = EmployeeRepo()

        # Шаг 2: Сохранение имени сотрудника и запрос даты рождения
        if not context.has_name:
            if message.text.strip() == "":
                bot.send_message(message.chat.id, "Это не имя. Напиши ещё раз.")
                return
            another_employee = employee_repo.find_by_name(message.text)
            if another_employee != None:
                bot.send_message(message.chat.id, "Такой сотрудник уже есть в базе. Его идентификатор {0}.".format(another_employee.id))
                clear_context(message)
                return
            context.employee.name = message.text
            context.has_name = True
            bot.send_message(message.chat.id, "А когда он родился? Формат даты: DD.MM.YYYY.")
        
        # Шаг 3: Сохранение даты рождения сотрудника и запись в БД
        else:
            try:
                context.employee.birthday = date_to_timestamp(parse_date(message.text))
            except:
                bot.send_message(message.chat.id, "Я не смог прочитать эту дату. Напиши ещё раз.")
                return
            employee_repo.add(context.employee)
            bot.send_message(message.chat.id, "Сотрудник {0} сохранён в базе! Его идентификатор {1}.".format(context.employee.name, context.employee.id))
            clear_context(message)


    @bot.message_handler(commands=["list"])
    @auth_org(bot)
    def list_employees(message):
        """
        Команда /list выводит список всех зарегистрированных сотрудников
        """

        clear_context(message)
        employee_repo = EmployeeRepo()
        employees = employee_repo.find_all()
        bot.send_message(message.chat.id, "\n".join(map(lambda x: "{0}\t{1}\t\tСледующий ДР: {2}".format(x.id, x.name, calc_next_birthday(timestamp_to_date(x.birthday))), employees)))


    @bot.message_handler(commands=["birthdays"])
    @auth_org(bot)
    def list_birthdays(message):
        """
        Команда /birthdays выводит список ближайших дней рождений
        """

        clear_context(message)
        employee_repo = EmployeeRepo()
        employees = employee_repo.find_all()
        employees = map(lambda x: (x, calc_next_birthday(timestamp_to_date(x.birthday))), employees)
        employees = map(lambda x: (x[0], x[1], x[1] - now()), employees)
        employees = filter(lambda x: x[2].days < 60, employees)
        employees = list(employees)
        employees.sort(key=lambda x: x[1])
        if len(employees) > 0:
            bot.send_message(message.chat.id, "\n".join(map(lambda x: "{0} - {1} (осталось {2} дней)".format(x[0].name, x[1], x[2].days), employees)))
        else:
            bot.send_message(message.chat.id, "В ближайшее время не ожидается дней рождений")


    @bot.message_handler(commands=["addorg"])
    @auth_org(bot)
    def add_org(message):
        """
        Команда /addorg добавляет нового организатора дней рождений
        """

        clear_context(message)

        #Шаг 1: Запрос имени или идентификатора сотрудника
        contexts[message.chat.id] = AddOrgContext()
        bot.send_message(message.chat.id, "Напиши, как зовут сотрудника, либо его идентификатор.")


    @bot.message_handler(func=lambda message: is_proper_context(message, AddOrgContext))
    @auth_org(bot)
    def continue_add_org(message):
        """
        Продолжение работы команды /addorg
        """

        context = contexts[message.chat.id]
        employee_repo = EmployeeRepo()
        org_repo = OrgRepo()

        #Шаг 2: Попытка найти сотрудника с таким именем или идентификатором
        employee = None
        if message.text.isdigit():
            employee = employee_repo.find_by_id(int(message.text))
        else:
            employees = employee_repo.find_by_part_of_name(message.text)
            if len(employees) == 1:
                employee = employees[0]
            elif len(employees) > 1:
                bot.send_message(message.chat.id, "Я нашёл несколько сотрудников с таким именем:\n{0}\nУточни имя.".format("\n".join(map(lambda x: x.name, employees))))
                return
        if employee == None:
            bot.send_message(message.chat.id, "Я не нашёл подходящего сотрудника.")
            clear_context(message)
            return

        #Шаг 3: Регистрация организатора
        org = org_repo.find_by_employee_id(employee.id)
        if org != None:
            bot.send_message(message.chat.id, "{0} уже является организатором дней рождений.".format(employee.name))
            clear_context(message)
            return
        org = Org(employee.id, 0, generate_secret_code())
        org_repo.add(org)
        bot.send_message(message.chat.id, "{0} стал организатором дней рождений. Не забудь отправить ему секретный код: `{1}`.".format(employee.name, org.secret_code))


    @bot.message_handler(func=lambda message: True)
    @auth_org(bot)
    def help(message):
        """
        Вызов справки - команда по умолчанию
        """
        
        clear_context(message)
        bot.send_message(message.chat.id, "\n".join([
            "/add - Добавить нового сотрудника",
            "/list - Показать всех сотрудников",
            "/birthdays - Показать ближайшие дни рождения",
            "",
            "/addorg - Добавить организатора дней рождений",
            "",
            "/cancel - Отмена текущей команды"
        ]))


    bot.polling()


if __name__ == "__main__":
    main()
