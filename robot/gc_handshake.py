# -*- coding=utf-8 -*- #

from robot.base_message import BaseMessage


class GCHandshake(BaseMessage):
    def __init__(self):
        super().__init__(self, 511)

    def read_impl(self, io_buffer):
        pass
