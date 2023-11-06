"""Run handler."""

import json

import tornado
from jupyter_server.base.handlers import APIHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin

from ..._version import __version__



# pylint: disable=W0223
class RunHandler(ExtensionHandlerMixin, APIHandler):
    """The run handler."""

    @tornado.web.authenticated
    def get(self):
        """Returns the run."""
        pass
