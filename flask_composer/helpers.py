import os
import flask

__author__ = 'Denis'


class Helper:
    def __init__(self, container):
        self.container = container
        self.endpoint_cache = {}

    def parts(self, name, before='', after=''):
        return '\n'.join(before + part + after for part in self.container.parts(name))

    def _static_endpoint(self, path):
        name = 'static'
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
        url = flask.url_for(self._static_endpoint(path), filename=path)
        return '<script type="text/javascript" src="{0}"></script>'.format(url)

    def styles(self, path):
        url = flask.url_for(self._static_endpoint(path), filename=path)
        return '<link rel="stylesheet" type="text/css" media="all" href="{0}"/>'.format(url)

    def action(self, title, action):
        url = flask.url_for(action)
        return '<a href="{0}">{1}</a>'.format(url, title)
