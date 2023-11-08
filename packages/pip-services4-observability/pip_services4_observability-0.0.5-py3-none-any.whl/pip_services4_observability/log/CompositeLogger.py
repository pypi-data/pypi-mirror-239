# -*- coding: utf-8 -*-
"""
    pip_services4_observability.log.CompositeLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Composite logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Optional

from pip_services4_components.context.IContext import IContext
from pip_services4_components.refer import IReferenceable, IReferences, Descriptor

from pip_services4_observability.log import LogLevel
from .ILogger import ILogger
from .Logger import Logger


class CompositeLogger(Logger, IReferenceable):
    """
    Aggregates all loggers from component references under a single component.

    It allows to log messages and conveniently send them to multiple destinations.

    ### References ###
        - `*:logger:*:*:1.0` 	(optional) :class:`ILogger <pip_services4_observability.log.ILogger.ILogger>` components to pass log messages

    Example:

    .. code-block:: python

        class MyComponent(IConfigurable, IReferenceable):
            __logger = CompositeLogger()

            def configure(self, config):
                self.__logger.configure(config)

            def set_references(self, references):
                self.__logger.set_references(references)

            def my_method(self, context):
                self.__logger.debug(context, "Called method mycomponent.mymethod")

    """

    def __init__(self, references: IReferences = None):
        """
        Creates a new instance of the logger.

        :param references: references to locate the component dependencies.
        """
        super().__init__()
        self.__loggers = []

        if not (references is None):
            self.set_references(references)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        super(CompositeLogger, self).set_references(references)
        # descriptor = Descriptor(None, "logger", None, None, None)
        loggers = references.get_optional(Descriptor(None, "logger", None, None, None))
        for logger in loggers:
            if isinstance(logger, ILogger):
                self.__loggers.append(logger)

    def _write(self, level: LogLevel, context: Optional[IContext], error: Optional[Exception],
               message: Optional[str]):
        """
        Writes a log message to the logger destination.

        :param level: a log level.

        :param context: (optional) transaction id to trace execution through call chain.

        :param error: an error object associated with this message.

        :param message: a human-readable message to log.
        """
        for logger in self.__loggers:
            logger.log(level, context, error, message)
