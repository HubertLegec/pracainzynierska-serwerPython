import logging


class LogFactory:
    ROOT_LOGGER_NAME = 'vse'
    FORMATTER = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s : %(message)s')
    DEFAULT_LOGge_LEVEL = 'INFO'
    DEFAULT_LOG_FILE = 'logs'

    @classmethod
    def get_logger(cls, config):
        log_config = config['logging']
        log = logging.getLogger(cls.ROOT_LOGGER_NAME)
        log.setLevel(logging.DEBUG)
        fh = cls._get_file_logger(log_config)
        ch = cls._get_console_logger(log_config)
        if fh:
            log.addHandler(fh)
        if ch:
            log.addHandler(ch)
        return log

    @classmethod
    def _get_file_logger(cls, config):
        if config['file_logs'] == 'yes':
            log_level = cls.DEFAULT_LOG_LEVEL
            if config['file_log_level']:
                log_level = config['file_log_level']
            log_file = cls.DEFAULT_LOG_FILE
            if config['log_file']:
                log_file = config['log_file']
            log = logging.FileHandler(log_file)
            log.setLevel(log_level)
            log.setFormatter(cls.FORMATTER)
            return log
        return None

    @classmethod
    def _get_console_logger(cls, config):
        if config['console_logs'] == 'yes':
            log_level = cls.DEFAULT_LOG_LEVEL
            if config['console_log_level']:
                log_level = config['console_log_level']
            log = logging.StreamHandler()
            log.setLevel(log_level)
            log.setFormatter(cls.FORMATTER)
            return log
        return None
