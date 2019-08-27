from __future__ import absolute_import

try:
    from requests import Session
except ImportError:
    Session = None

from speedbar.modules.base import BaseModule, RequestTrace
from speedbar.modules.stacktracer import trace_method


ENTRY_TYPE = 'requests'


class RequestsModule(BaseModule):
    key = 'requests'

    def get_metrics(self):
        return RequestTrace.instance().stacktracer.get_node_metrics('REQUESTS')

    def get_details(self):
        nodes = RequestTrace.instance().stacktracer.get_nodes('REQUESTS')
        return [
            {'method': node.label, 'time': node.duration}
            for node in nodes
        ]


def init():
    if Session is None:
        return False

    # The linter thinks the methods we monkeypatch are not used
    # pylint: disable=W0612
    @trace_method(Session)
    def request(self, method, *args, **kwargs):
        return ('REQUESTS', method, {})

    return RequestsModule
