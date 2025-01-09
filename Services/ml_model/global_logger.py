import logging

class GlobalLogger:
    def __init__(self, log_file=None):
        self.logger = logging.getLogger('global_logger')
        self.logger.setLevel(logging.DEBUG)
        
        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # Create file handler if log_file is provided
        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(data)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(data)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def info(self, message, extra=None):
        if extra is None:
            extra = {}
        if 'data' not in extra:
            extra['data'] = 'N/A'
        self.logger.info(message, extra=extra)

    def warning(self, message, extra=None):
        if extra is None:
            extra = {}
        if 'data' not in extra:
            extra['data'] = 'N/A'
        self.logger.warning(message, extra=extra)

    def error(self, message, extra=None):
        if extra is None:
            extra = {}
        if 'data' not in extra:
            extra['data'] = 'N/A'
        self.logger.error(message, extra=extra)

    def debug(self, message, extra=None):
        if extra is None:
            extra = {}
        if 'data' not in extra:
            extra['data'] = 'N/A'
        self.logger.debug(message, extra=extra)

# Create a global logger instance
global_logger = GlobalLogger()