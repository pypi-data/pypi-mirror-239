# -*- coding: utf-8 -*-
import time

from pip_services4_components.context import Context
from pip_services4_observability.log import LogLevel


class LoggerFixture:
    def __init__(self, logger):
        self.__logger = logger

    def test_log_level(self):
        assert self.__logger.get_level() >= LogLevel.Nothing
        assert self.__logger.get_level() <= LogLevel.Trace

    def test_simple_logging(self):
        ctx = Context.from_trace_id('test')
        self.__logger.set_level(LogLevel.Trace)

        self.__logger.fatal(ctx, None, 'Fatal error message')
        self.__logger.error(ctx, None, 'Error message')
        self.__logger.warn(ctx, 'Warning message')
        self.__logger.info(ctx, 'Information message')
        self.__logger.debug(ctx, 'Debug message')
        self.__logger.trace(ctx, 'Trace message')

        self.__logger.dump()
        time.sleep(1)

    def test_error_logging(self):
        ctx = Context.from_trace_id('test')

        try:
            # Raise an exception
            raise Exception('test')
        except Exception as err:
            self.__logger.fatal(ctx, err, 'Fatal error')
            self.__logger.error(ctx, err, 'Recoverable error')
            assert err is not None

        self.__logger.dump()
        time.sleep(1)
