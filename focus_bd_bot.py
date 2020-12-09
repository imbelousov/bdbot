#!/usr/bin/env python
import configparser
import telebot

config = configparser.ConfigParser()
config.read("focus_bd_bot.ini")
bot = telebot.TeleBot(config["Api"]["Token"])


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Hello, world!")


bot.polling()
