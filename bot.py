import logging
import os

from icq.bot import ICQBot
from icq.constant import TypingStatus
from icq.handler import (
    FeedbackCommandHandler, HelpCommandHandler, TypingHandler
)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)


def help_cb(bot, event):
    source = event.data.get("aimId") or event.data["source"]["aimId"]
    (command, command_body) = event.data["message"].partition(" ")[::2]
    bot.send_im(
        target=source,
        message="Command '{message}' with body '{command_body}' received from '{source}'.".format(
            source=source, message=command[1:], command_body=command_body
        )
    )


def typing_cb(bot, event):
    source = event.data["aimId"]
    bot.send_im(target=source, message="Typing status '{typing_status}' received from user {source}.".format(
        source=source, typing_status=TypingStatus(event.data["typingStatus"]).value
    ))


def main():
    # Creating a new bot instance.
    TOKEN = os.environ['bot_token']
    NAME = os.environ['bot_name']
    VERSION = os.environ['bot_version']
    OWNER = os.environ['bot_owner']

    logger.info("start to init")

    bot = ICQBot(token=TOKEN, name=NAME, version=VERSION)
    bot.dispatcher.add_handler(HelpCommandHandler(callback=help_cb))
    bot.dispatcher.add_handler(TypingHandler(typing_cb))

    # Registering command handlers.
    bot.dispatcher.add_handler(FeedbackCommandHandler(target=OWNER))

    logger.info("wake up")
    # Starting a polling thread watching for new events from server. This is a non-blocking call.
    bot.start_polling()

    logger.info("listening")
    # Blocking the current thread while the bot is working until SIGINT, SIGTERM or SIGABRT is received.
    bot.idle()


if __name__ == "__main__":
    main()
