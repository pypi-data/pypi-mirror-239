import sys, os, re
from loguru import logger as loguer

loguercor = loguer.opt(colors=True)

level_dict = {
    'CRITICAL': "1",
    'Print': "1",
    'ERROR': "2",
    'WARNING': "3",
    "SUCCESS": "3",
    'Crawl': "4",
    'Start': "4",
    'Close': "4",
    "INFO": "4",
    "DEBUG": "5",
}


def get_level(level):
    level_list = []
    for k, v in level_dict.items():
        if level >= int(v):
            level_list.append(k)
    return level_list


class Log():
    def __init__(self, log_stdout=True, log_level='INFO', log_file=False) -> None:
        self.level_dict = {
            "warn": 'WARNING',
            "info": 'INFO',
            "debug": 'DEBUG',
            "error": 'ERROR',
            "critical": 'CRITICAL',
            "success": 'SUCCESS',
        }
        self.level_stdout = {
            "critical": get_level(1),
            "error": get_level(2),
            "success": get_level(3),
            "warn": get_level(3),
            "info": get_level(4),
            "debug": get_level(5),
        }
        self.log_stdout, self.log_level, self.log_file = log_stdout, log_level, log_file
        loguer.level("DEBUG", color="<green>")
        loguer.level("INFO", color="<cyan>")
        loguer.level("SUCCESS", color="<light-green>")
        loguer.level("WARNING", color="<yellow>")
        loguer.level("ERROR", color="<red>")
        loguer.level("CRITICAL", color="<red>")
        loguer.level("Print", no=30, color="<green>")
        loguer.level("Crawl", no=40, color="<green>")
        loguer.level("Start", no=50, color="<yellow>")
        loguer.level("Close", no=50, color="<yellow>")
        loguer.level("End", no=50, color="<red>")

    def loggering(self):
        levels = self.level_dict.get(self.log_level.lower())
        slevel = self.level_stdout.get(self.log_level.lower())
        format = "<b><green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green></b><b><level> | {level: ^8} | </level></b><b><i>{message}</i></b>"
        stdout_handler = {
            "sink": sys.stdout,
            "colorize": True,
            "filter": lambda record: record["level"].name in slevel,
            "format": format
        }
        loguer.configure(handlers=[stdout_handler])
        if self.log_stdout:
            sys.stdout = InterceptHandler()
        if self.log_file:
            file_log = os.path.basename(__file__) if self.log_file is True else self.log_file
            file_log = (
                re.sub("\..*", ".log", file_log)
                if "." in file_log
                else file_log + ".log"
            )
            filename = f"./{file_log}"
            loguer.add(filename, level=levels, format=format)
        return loguer


class InterceptHandler():
    def write(self, message):
        if message.strip():
            loguer.log("Print", message.strip())

    def flush(self):
        pass


class loging:
    def __init__(self, log):
        self.loger = log

    def print(self, msg):
        self.loger.log('Print', msg)

    def info(self, msg):
        self.loger.info(msg)

    def warn(self, msg):
        self.loger.warn(msg)

    def error(self, msg):
        self.loger.error(msg)

    def debug(self, msg):
        self.loger.debug(msg)

    def success(self, msg):
        self.loger.success(msg)

    def critical(self, msg):
        self.loger.critical(msg)
