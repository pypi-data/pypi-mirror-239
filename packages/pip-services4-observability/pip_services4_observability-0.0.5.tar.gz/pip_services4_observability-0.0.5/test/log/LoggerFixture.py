# -*- coding: utf-8 -*-
"""
    tests.logs.LoggerFixture
    ~~~~~~~~~~~~~~~~~~~~~~~~
    
    :copyright: (c) Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services4_components.context import Context

from pip_services4_observability.log import LogLevel


class LoggerFixture:
    _logger = None

    def __init__(self, logger):
        self._logger = logger

    def test_log_level(self):
        assert self._logger.get_level() >= LogLevel.Nothing
        assert self._logger.get_level() <= LogLevel.Trace

    def test_text_output(self):
        self._logger.log(LogLevel.Fatal, Context.from_trace_id("123"), None, "Fatal error...")
        self._logger.log(LogLevel.Error, Context.from_trace_id("123"), None, "Recoverable error...")
        self._logger.log(LogLevel.Warn, Context.from_trace_id("123"), None, "Warning...")
        self._logger.log(LogLevel.Info, Context.from_trace_id("123"), None, "Information message...")
        self._logger.log(LogLevel.Debug, Context.from_trace_id("123"), None, "Debug message...")
        self._logger.log(LogLevel.Trace, Context.from_trace_id("123"), None, "Trace message...")
