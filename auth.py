#!/usr/bin/env python
from telebot import TeleBot
from orgs import Org, OrgRepo


def auth_org(bot: TeleBot):
    def __auth_org(func):
        def wrapper(message):
            org_repo = OrgRepo()
            org = org_repo.find_by_chat_id(message.chat.id)
            if org == None:
                bot.send_message(message.chat.id, "Вы не авторизованы как организатор. Для авторизации используйте команду /auth.")
                return
            return func(message)
        return wrapper
    return __auth_org
