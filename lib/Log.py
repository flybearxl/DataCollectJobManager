# --coding:utf-8--

import os
import sys


class load_log():
    def __init__(self, log_name):
        self.log = open(log_name, 'r')

    def read(self, position):
        log_content = []
        for log in self.log.readlines():
            log_content.append()
            return log_content[position:]
        self.log.close()
