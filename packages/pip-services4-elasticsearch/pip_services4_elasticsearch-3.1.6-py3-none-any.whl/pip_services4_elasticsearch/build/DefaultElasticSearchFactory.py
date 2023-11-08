# -*- coding: utf-8 -*-

from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from ..log import ElasticSearchLogger


class DefaultElasticSearchFactory(Factory):
    """
    Creates ElasticSearch components by their descriptors.

    See :class:`ElasticSearchLogger <log.ElasticSearchLogger>`
    """
    __ElasticSearchLoggerDescriptor = Descriptor("pip-services", "logger", "elasticsearch", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultElasticSearchFactory, self).__init__()
        self.register_as_type(self.__ElasticSearchLoggerDescriptor, ElasticSearchLogger)
