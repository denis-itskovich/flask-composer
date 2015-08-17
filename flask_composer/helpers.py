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
        key = '{0}@{1}'.format(name, path)
        if key in self.endpoint_cache:
            return self.endpoint_cache[key]

        endpoint = name

        component = self.container.current_component
        if component is not None:
            file = os.path.join(self.container.blueprints[component.name].root_path, name, path)
            if os.path.exists(file):
                endpoint = '{0}.{1}'.format(component.name, name)

        self.endpoint_cache[key] = endpoint
        return endpoint

    def script(self, path):
        url = url_for(self._endpoint('static', path), filename=path)
        return '<script type="text/javascript" src="{0}"></script>'.format(url)

    def styles(self, path):
        url = url_for(self._endpoint('static', path), filename=path)
        return '<link rel="stylesheet" type="text/css" media="all" href="{0}"/>'.format(url)
