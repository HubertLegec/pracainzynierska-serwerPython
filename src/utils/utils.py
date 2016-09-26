import logging


def get_logger(name, level):
    log = logging.getLogger(name)
    log.setLevel(level)
    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log
