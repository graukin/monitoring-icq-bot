from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import logging
import json
import errno
import os


class MessageOperator(BaseOperator):
    """
    Example of an operator for Airflow.
    Arguments: label and message.
    Always runs on 'master' queue. If not, forced changes given queue on 'master'.
    Use named pipe /tmp/bot_msgs for communications with bot (look into config.json - bot reads from it)
    """
    template_fields = tuple()
    ui_color = '#f7c285'

    def send_bot_message(self):
        msg = json.dumps({"lbl": self.label, "msg": self.message})
        fifo_file = "/tmp/bot_msgs"
        try:
            os.mkfifo(fifo_file)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                raise

        with open(fifo_file, "w") as fifo:
            fifo.write(msg)
            fifo.flush()
        return 0

    @apply_defaults
    def __init__(self, label, message, *args, **kwargs):
        if "queue" not in kwargs or kwargs["queue"] is not "master":
            logging.info("Wrong queue - only \"master\" is allowed. Replace it.")
            kwargs["queue"] = "master"
        super(MessageOperator, self).__init__(*args, **kwargs)
        self.label = label
        self.message = message

    def execute(self, context):
        return_value = self.send_bot_message()
        logging.info("Message sent. Returned value was: {0}".format(return_value))
        return return_value
