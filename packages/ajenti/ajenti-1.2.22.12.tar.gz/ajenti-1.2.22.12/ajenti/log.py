import logging
import logging.handlers
import os
import sys
from datetime import datetime

from ajenti.api import extract_context


LOG_DIR = '/var/log/ajenti'
LOG_NAME = 'ajenti.log'
LOG_FILE = os.path.join(LOG_DIR, LOG_NAME)


class DebugHandler (logging.StreamHandler):
    """
    Captures log into a buffer for error reports
    """

    def __init__(self):
        self.capturing = False
        self.buffer = ''

    def start(self):
        self.capturing = True

    def stop(self):
        self.capturing = False

    def handle(self, record):
        if self.capturing:
            self.buffer += self.formatter.format(record) + '\n'


class ConsoleHandler (logging.StreamHandler):
    def __init__(self, stream, debug):
        self.debug = debug
        logging.StreamHandler.__init__(self, stream)

    def handle(self, record):
        if not self.stream.isatty():
            return logging.StreamHandler.handle(self, record)

        s = ''
        d = datetime.fromtimestamp(record.created)
        s += d.strftime("\033[37m%d.%m.%Y %H:%M \033[0m")
        if self.debug:
            s += ('%s:%s' % (record.filename, record.lineno)).ljust(30)
        l = ''
        if record.levelname == 'DEBUG':
            l = '\033[37mDEBUG\033[0m '
        if record.levelname == 'INFO':
            l = '\033[32mINFO\033[0m  '
        if record.levelname == 'WARNING':
            l = '\033[33mWARN\033[0m  '
        if record.levelname == 'ERROR':
            l = '\033[31mERROR\033[0m '
        s += l.ljust(9)

        context = extract_context()
        if hasattr(context, 'session') and hasattr(context.session, 'identity'):
            s += '[%s] ' % context.session.identity

        try:
            s += record.msg % record.args
        except:
            s += record.msg
        s += '\n'
        self.stream.write(s)


def make_log(debug=False, log_level=logging.INFO):
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    stdout = ConsoleHandler(sys.stdout, debug)
    stdout.setLevel(log_level)

    logging.blackbox = DebugHandler()
    logging.blackbox.setLevel(logging.DEBUG)
    dformatter = logging.Formatter('%(asctime)s %(levelname)-8s %(module)s.%(funcName)s(): %(message)s')
    logging.blackbox.setFormatter(dformatter)
    stdout.setFormatter(dformatter)
    log.addHandler(logging.blackbox)

    log.addHandler(stdout)


def init_log_directory():
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)


def init_log_rotation():
    log = logging.getLogger()
    try:
        handler = logging.handlers.TimedRotatingFileHandler(
            os.path.join(LOG_DIR, LOG_NAME),
            when='midnight',
            backupCount=7
        )
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s'))
        log.addHandler(handler)
    except IOError:
        pass

    return log


def init(level=logging.INFO):
    make_log(debug=level == logging.DEBUG, log_level=level)
    logging.blackbox.start()
