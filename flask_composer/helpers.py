import os
from flask import url_for, request

__author__ = 'Denis'


class Helper:
    def __init__(self, container):
        self.container = container
        self.endpoint_cache = {}

    def parts(self, name):
        return '\n'.join(self.container.parts(name))

    def _endpoint(self, name, path):
        key = '{}@{}'.format(name, path)
        if key in self.endpoint_cache:
            return self.endpoint_cache[key]

        endpoint = name

        plugin = self.container.current_plugin
        if plugin is not None:
            file = os.path.join(self.container.blueprints[plugin.name].root_path, name, path)
            if os.path.exists(file):
                endpoint = '{}.{}'.format(plugin.name, name)

        self.endpoint_cache[key] = endpoint
        return endpoint

    def script(self, path):
        url = url_for(self._endpoint('static', path), filename=path)
        return '<script type="text/javascript" src="{}"></script>'.format(url)

    def styles(self, path):
        url = url_for(self._endpoint('static', path), filename=path)
        return '<link rel="stylesheet" type="text/css" media="all" href="{}"/>'.format(url)
