import logging
import sys


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