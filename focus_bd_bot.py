#!/usr/bin/env python
import configparser
import telebot
from orgs import Org, OrgRepo

config = configparser.ConfigParser()
config.read("focus_bd_bot.ini")
bot = telebot.TeleBot(config["Api"]["Token"])
org_repo = OrgRepo(config["Sqlite"]["FileName"])


def get_current_org(chat_id: int) -> Org:
    org = org_repo.find_by_chat_id(chat_id)
    if org != None:
        return org
    id = org_repo.create(chat_id)
    return Org(id=id, chat_id=chat_id, name=None)


@bot.message_handler(commands=["start"])
def start_message(message):
    org = get_current_org(message.chat.id)
    bot.send_message(message.chat.id, "Hello, world! Chat id: {0}, org id: {1}".format(org.chat_id, org.id))


bot.polling()
