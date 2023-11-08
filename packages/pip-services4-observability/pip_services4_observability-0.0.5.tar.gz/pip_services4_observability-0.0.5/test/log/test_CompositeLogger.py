# -*- coding: utf-8 -*-
"""
    tests.log.test_CompositeLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    :copyright: (c) Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services4_components.refer import References, Descriptor

from pip_services4_observability.log import CompositeLogger
from pip_services4_observability.log import ConsoleLogger
from pip_services4_observability.log import NullLogger
from .LoggerFixture import LoggerFixture


class TestCompositeLogger:
    log = None
    fixture = None

    def setup_method(self, method):
        refs = References.from_tuples(
            Descriptor("pip-services", "logger", "null", "default", "1.0"), NullLogger(),
            Descriptor("pip-services", "logger", "console", "default", "1.0"), ConsoleLogger()
        )

        self.log = CompositeLogger(refs)
        self.fixture = LoggerFixture(self.log)

    def test_log_level(self):
        self.fixture.test_log_level()

    def test_text_output(self):
        self.fixture.test_text_output()
