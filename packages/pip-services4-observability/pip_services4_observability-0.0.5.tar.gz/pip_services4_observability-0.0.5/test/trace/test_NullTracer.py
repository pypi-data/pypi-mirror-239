# -*- coding: utf-8 -*-
from pip_services4_components.context import Context

from pip_services4_observability.trace.NullTracer import NullTracer


class TestNullTracer:
    _tracer: NullTracer

    def setup_method(self):
        self._tracer = NullTracer()

    def test_simple_tracing(self):
        self._tracer.trace(Context.from_trace_id("123"), "mycomponent", "mymethod", 123456)
        self._tracer.failure(Context.from_trace_id("123"), "mycomponent", "mymethod", Exception("Test error"), 123456)

    def test_trace_timing(self):
        timing = self._tracer.begin_trace(Context.from_trace_id("123"), "mycomponent", "mymethod")
        timing.end_trace()

        timing = self._tracer.begin_trace(Context.from_trace_id("123"), "mycomponent", "mymethod")
        timing.end_failure(Exception("Test error"))
