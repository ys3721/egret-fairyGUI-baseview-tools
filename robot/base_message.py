# -*- encoding=utf8 -*- #
import robot.bytes_utils as bytes_utils


class BaseMessage:
    def __init__(self, message_type):
        self.message_type = message_type

    def get_message_type(self):
        return self.message_type

