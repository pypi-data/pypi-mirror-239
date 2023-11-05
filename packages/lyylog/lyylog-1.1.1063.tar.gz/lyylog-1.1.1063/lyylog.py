#1.10.21

from datetime import datetime
import sys, os

import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = None

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)
os.chdir(script_dir)

exe_file_name = os.path.basename(sys.argv[0])
log_filename_prefix = f"log_{exe_file_name }.log"
print("log filename  is ", log_filename_prefix)


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def log(message, if_print=True):
    #fastest way to logging to the module what called this function. like log_mudule_name.log.
    #This log file is readable and writable (cannot be deleted by other similar modules at runtime), and its name will change as the log evolves.

    if if_print:
        print(message)
    global handler
    if handler is None:
        today = datetime.now().strftime("%Y-%m-%d")
        handler = CustomTimedRotatingFileHandler(f'lyylog_{log_filename_prefix}_{today}.log', when='midnight', interval=1, backupCount=7)
        handler.suffix = "%Y-%m-%d"
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    with handler:
        logger.info(str(message))


def logg(log_filename_prefix, message, if_print=True):
    #logg can define log filename by youself
    if if_print:
        print(message)
    global handler
    if handler is None:
        today = datetime.now().strftime("%Y-%m-%d")
        handler = CustomTimedRotatingFileHandler(f'lyylog_{log_filename_prefix}_{today}.log', when='midnight', interval=1, backupCount=7)
        handler.suffix = "%Y-%m-%d"
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    with handler:
        logger.info(str(message))


def logwithdir(dirname, message, if_print=True):
    #fastest way to logging to the module what called this function. like log_mudule_name.log.
    #This log file is readable and writable (cannot be deleted by other similar modules at runtime), and its name will change as the log evolves.
    log_filename_prefix = os.path.basename(sys.argv[0])
    if if_print:
        print(message)
    global handler
    if handler is None:
        today = datetime.now().strftime("%Y-%m-%d")
        handler = CustomTimedRotatingFileHandler(f'{dirname}/lyylog_{log_filename_prefix}_{today}.log', when='midnight', interval=1, backupCount=7)
        handler.suffix = "%Y-%m-%d"
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    with handler:
        logger.info(str(message))


def run_with_error_handling(func):
    try:
        func()
    except Exception as e:
        # 处理异常，可以打印日志或执行其他操作
        log(f"模块 {func.__name__} 出现异常: {e}")


if __name__ == '__main__':
    # exit()
    log("testest")
