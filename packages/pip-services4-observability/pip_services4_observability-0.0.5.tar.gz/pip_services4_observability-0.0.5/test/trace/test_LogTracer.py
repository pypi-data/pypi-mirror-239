# -*- coding: utf-8 -*-
from pip_services4_components.context import Context
from pip_services4_components.refer import References, Descriptor

from pip_services4_observability.log import NullLogger
from pip_services4_observability.trace.LogTracer import LogTracer


class TestLogTracer:
    _tracer: LogTracer

    def setup_method(self):
        self._tracer = LogTracer()
        self._tracer.set_references(References.from_tuples(
            Descriptor("pip-services", "logger", "null", "default", "1.0"), NullLogger()
        ))

    def test_simple_tracing(self):
        self._tracer.trace(Context.from_trace_id("123"), "mycomponent", "mymethod", 123456)
        self._tracer.failure(Context.from_trace_id("123"), "mycomponent", "mymethod", Exception("Test error"), 123456)

    def test_trace_timing(self):
        timing = self._tracer.begin_trace(Context.from_trace_id("123"), "mycomponent", "mymethod")
        timing.end_trace()

        timing = self._tracer.begin_trace(Context.from_trace_id('123'), "mycomponent", "mymethod")
        timing.end_failure(Exception('Test error'))
