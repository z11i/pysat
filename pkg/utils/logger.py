import logging
import sys

logging.FINE = 7
logging.FINER = 5
logging.FINEST = 1

logging.addLevelName(logging.FINE, 'FINE')
logging.addLevelName(logging.FINER, 'FINER')
logging.addLevelName(logging.FINEST, 'FINEST')


def fine(self, message, *args, **kws):
    if self.isEnabledFor(logging.FINE):
        self._log(logging.FINE, '\t{}'.format(message), args, **kws)


def finer(self, message, *args, **kws):
    if self.isEnabledFor(logging.FINER):
        self._log(logging.FINER, '\t\t{}'.format(message), args, **kws)


def finest(self, message, *args, **kws):
    if self.isEnabledFor(logging.FINEST):
        self._log(logging.FINEST, '\t\t\t{}'.format(message), args, **kws)


logging.Logger.fine = fine
logging.Logger.finer = finer
logging.Logger.finest = finest


def set_logger(level='DEBUG'):
    """
    Sets the class logger
        :param level: the level int for logging, defaults to DEBUG
    """
    log = logging.getLogger(__name__)
    log.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(funcName)s][%(levelname)s]: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log