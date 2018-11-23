import logging.config

from threading import Thread

import os
import errno

import json
from icq.bot import ICQBot
from icq.filter import MessageFilter
from icq.handler import CommandHandler, MessageHandler, UnknownCommandHandler

from processing.db_wrapper import DBWrapper

from enum import Enum

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

db_wrapper = DBWrapper()


class BotStates(Enum):
    HALT = 1
    ADD_LABEL = 2
    REMOVE_LABEL = 3


bot_state = BotStates.HALT

with open('./resources/config.json', 'r') as f:
    config = json.load(f)


def help_cb(bot, event):
    logging.debug("Send help.")

    user_id = event.data["source"]["aimId"]
    bot.send_im(target=user_id,
                message="/list - get all your labels.\n"
                        "/add - add new label.\n"
                        "/rm - remove one of your labels.\n"
                        "/help - get this message.\n")


def message_cb(bot, event):
    logging.debug("Message received.")

    user_id = event.data["source"]["aimId"]
    logging.debug(user_id)

    data = event.data["message"]

    global bot_state
    if bot_state == BotStates.ADD_LABEL:
        res = db_wrapper.add_label(user_id, data)
        if res == 0:
            bot.send_im(target=user_id,
                        message="No new label was added.")
        elif res == 1:
            bot.send_im(target=user_id,
                        message="New label '{0}' was added to your list.".format(data))
            db_wrapper.save_file()
        elif res == 2:
            bot.send_im(target=user_id,
                        message="User '{0}' was just registered. New label '{1}' was added to your list.".format(user_id, data))
            db_wrapper.save_file()
    elif bot_state == BotStates.REMOVE_LABEL:
        res = db_wrapper.remove_label(user_id, data)
        if res == -1:
            bot.send_im(target=user_id,
                        message="No more labels left behind. User '{0}' was just unregistered.".format(user_id))
            db_wrapper.save_file()
        elif res == 0:
            bot.send_im(target=user_id,
                        message="You have no label '{0}' in the list.".format(data))
        else:
            bot.send_im(target=user_id,
                        message="Remove all occurrences of label '{0}'.".format(data))
            db_wrapper.save_file()

    bot_state = BotStates.HALT


def list_labels_cb(bot, event):
    logging.debug("Command received, list my labels.")

    user_id = event.data["source"]["aimId"]
    logging.debug(user_id)
    labels = db_wrapper.search_by_user(user_id)
    bot.send_im(target=user_id, message="Registered labels: {0}".format([x.encode('utf-8') for x in labels]))
    global bot_state
    bot_state = BotStates.HALT


def add_labels_cb(bot, event):
    logging.debug("Command received, add label.")

    user_id = event.data["source"]["aimId"]
    logging.debug(user_id)
    bot.send_im(target=user_id, message="Type label you'd like to add:")
    global bot_state
    bot_state = BotStates.ADD_LABEL


def rm_labels_cb(bot, event):
    logging.debug("Command received, remove label.")

    user_id = event.data["source"]["aimId"]
    logging.debug(user_id)
    bot.send_im(target=user_id, message="Type label you'd like to remove:")
    global bot_state
    bot_state = BotStates.REMOVE_LABEL


def listen_pipe(bot):
    file = config['PIPE_FILE']
    try:
        os.mkfifo(file)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise

    while True:
        read_fifo(file, bot)


def read_fifo(file, bot):
    with open(file) as fifo:
        while True:
            data = fifo.read()
            if len(data) == 0:
                print("Writer closed")
                break
            msg = json.loads(data)
            if msg["lbl"]:
                users = db_wrapper.search_by_raw_label(msg["lbl"])
                for user_id in users:
                    bot.send_im(target=user_id, message="[{0}] {1}".format(msg["lbl"], msg["msg"]))


def main():
    db_wrapper.load_file()

    # Creating a new bot instance.
    bot = ICQBot(token=config['TOKEN'], name=config['NAME'], version=config['VERSION'])

    # Registering message handlers.
    bot.dispatcher.add_handler(MessageHandler(filters=MessageFilter.message, callback=message_cb))
    # Registering command handlers.
    bot.dispatcher.add_handler(CommandHandler(command="list", callback=list_labels_cb))
    bot.dispatcher.add_handler(CommandHandler(command="add", callback=add_labels_cb))
    bot.dispatcher.add_handler(CommandHandler(command="rm", callback=rm_labels_cb))
    # Registering help handler.
    bot.dispatcher.add_handler(UnknownCommandHandler(callback=help_cb))

    # Starting a polling thread watching for new events from server. This is a non-blocking call.
    bot.start_polling()

    t1 = Thread(target=listen_pipe, args=(bot,))
    t1.start()

    # Blocking the current thread while the bot is working until SIGINT, SIGTERM or SIGABRT is received.
    bot.idle()

    db_wrapper.save_file()


if __name__ == "__main__":
    main()
