# -*- coding=utf-8 -*- #

import robot.bytes_utils

from robot.base_message import BaseMessage


class CGHandshake(BaseMessage):
    def __init__(self):
        super().__init__(510)

    def read_impl(self, io_buffer):
        pass
