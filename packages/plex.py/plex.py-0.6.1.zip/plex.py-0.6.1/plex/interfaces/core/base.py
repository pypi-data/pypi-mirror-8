from plex.lib.six import string_types
from plex.lib.six.moves.urllib_parse import urlparse

from functools import wraps
import logging

try:
    from lxml import etree as ET
except ImportError:
    from xml.etree import ElementTree as ET

log = logging.getLogger(__name__)


class Interface(object):
    path = None
    object_map = {}

    def __init__(self, client):
        self.client = client

    def __getitem__(self, name):
        if hasattr(self, name):
            return getattr(self, name)

        raise ValueError('Unknown action "%s" on %s', name, self)

    @property
    def http(self):
        if not self.client:
            return None

        return self.client.http.configure(self.path)

    def parse(self, response, schema):
        if response.status_code < 200 or response.status_code >= 300:
            return None

        root = ET.fromstring(response.content)

        url = urlparse(response.url)
        path = url.path

        return self.__construct(self.client, path, root, schema)

    @classmethod
    def __construct(cls, client, path, node, schema):
        if not schema:
            return None

        item = schema.get(node.tag)

        if item is None:
            raise ValueError('Unknown node with tag "%s"' % node.tag)

        if type(item) is dict:
            value = node.get(item.get('_', 'type'))

            if value is None:
                return None

            item = item.get(value)

            if item is None:
                raise ValueError('Unknown node type "%s"' % value)

        descriptor = None
        child_schema = None

        if type(item) is tuple and len(item) == 2:
            descriptor, child_schema = item
        else:
            descriptor = item

        if isinstance(descriptor, string_types):
            if descriptor not in cls.object_map:
                raise Exception('Unable to find descriptor by name "%s"' % descriptor)

            descriptor = cls.object_map.get(descriptor)

        if descriptor is None:
            raise Exception('Unable to find descriptor')

        keys_used, obj = descriptor.construct(client, node, path=path)

        # Lazy-construct children
        def iter_children():
            for child_node in node:
                item = cls.__construct(client, path, child_node, child_schema)

                if item:
                    yield item

        obj._children = iter_children()

        return obj


class InterfaceProxy(object):
    def __init__(self, interface, args):
        self.interface = interface
        self.args = list(args)

    def __getattr__(self, name):
        value = getattr(self.interface, name)

        if not hasattr(value, '__call__'):
            return value

        @wraps(value)
        def wrap(*args, **kwargs):
            args = self.args + list(args)

            return value(*args, **kwargs)

        return wrap
