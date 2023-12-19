import logging


class GetLogger:
    _logger = None

    @staticmethod
    def get_logger():
        if GetLogger._logger is None:
            GetLogger._logger = logging.getLogger("market-streamline")
            GetLogger._logger.setLevel(logging.DEBUG)

            # Create handlers, formatters and add them to the logger
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '[%(asctime)s.%(msecs)03d] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            GetLogger._logger.addHandler(handler)

        return GetLogger._logger
