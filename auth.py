#!/usr/bin/env python
from telebot import TeleBot
from data.orgs import OrgRepo, Role


def auth_org(bot: TeleBot, min_role: int = Role.USER):
    def __auth_org(func):
        def wrapper(message):
            org_repo = OrgRepo()
            org = org_repo.find_by_chat_id(message.chat.id)
            if org == None:
                bot.send_message(message.chat.id, "Вы не авторизованы как организатор. Для авторизации используйте команду /auth.")
                return
            if org.role < min_role:
                bot.send_message(message.chat.id, "У вас недостаточно прав для вызова этой команды.")
                return
            return func(message)
        return wrapper
    return __auth_org
