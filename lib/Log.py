# --coding:utf-8--

import logging
from ManageJob import *
import time


class Log:
    def __init__(self):
        self.logger_info = None
        self.gen_logger()

    def gen_logger(self):
        self.logger_info = logging.getLogger("Data_Collect_Log")
        log_info_file = os.path.join(log_root_path, time.strftime('%Y%m%d', time.localtime()) + '.log')
        fh = logging.FileHandler(log_info_file)

        fmt = logging.Formatter("[%(asctime)s]-%(levelname)s:%(message)s")

        fh.setFormatter(fmt)
        fh.setLevel(logging.INFO)

        self.logger_info.addHandler(fh)
        self.logger_info.setLevel(logging.INFO)


if __name__ == '__main__':
    log = Log()
    log.save('error', '1')
