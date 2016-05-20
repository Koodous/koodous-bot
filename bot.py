# -*- coding: utf-8 -*-
import telegram
import requests
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from settings import *

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello!")

def search(bot, update):
    text = update.message.text.replace("/search ","")
    bot.sendMessage(chat_id=update.message.chat_id, text="Looking for apks with the string *%s*" % text, parse_mode=telegram.ParseMode.MARKDOWN)

    r = requests.get("https://api.koodous.com/apks?search=%s" % text)

    try:
        aux = r.json().get("results")[0]
    except:
        bot.sendMessage(chat_id=update.message.chat_id, text="There is no matches for the string *%s*" % text, parse_mode=telegram.ParseMode.MARKDOWN)
        return False
    
    response = """ %(app)s (%(package_name)s)
url: https://analyst.koodous.com/apks/%(sha256)s
"""

    bot.sendMessage(chat_id=update.message.chat_id, text=response % aux)


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))

updater.start_polling()
updater.idle()