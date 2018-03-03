#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import gmtime, strftime

import logging
import os
import subprocess
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN  = 'XXXXX'
MINERO1 = 'XXXXX'
MY_CHAT_ID = 'XXXXX'
ALIVE_STRING = 'Approximate round trip times in milli-seconds:'

def is_alive(address):
    output = subprocess.Popen(["ping.exe", "-n", "1", address],stdout = subprocess.PIPE).communicate()[0]
    if ALIVE_STRING not in output:
        return False
    return True

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! (WIP)')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def check1(bot, update):
    print "\nMessage received from: ", update.message.chat_id
    if is_alive(MINERO1):
        update.message.reply_text('MINERO1 is alive!')
    else:
        update.message.reply_text('MINERO1 is ded :(')

def pinger1(bot, update):
    if str(update.message.chat_id) != MY_CHAT_ID:
        update.message.reply_text('Sorry, this command is only available to my owner.')
        return
    start_msg = "pinger1 STARTED at %s" % strftime("%Y-%m-%d %H:%M:%S", gmtime())
    update.message.reply_text(start_msg)
    alive = True
    while alive:
        time.sleep(10)
        alive = is_alive(MINERO1)
    update.message.reply_text('MINERO1 went ded in the last 10 seconds, rip')
    end_msg = "pinger1 ENDS at %s" % strftime("%Y-%m-%d %H:%M:%S", gmtime())
    update.message.reply_text(end_msg)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("check1", check1))
    dp.add_handler(CommandHandler("pinger1", pinger1))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()