__author__ = 'Denis Itskovich'
__version__ = (0, 3, 1)

import os


class TemplatePathLookup:
    def __init__(self, dirs, parent=None):
        self.dirs = [self._combine_path(d) for d in dirs]
        self.template_cache = {}
        self.parent = parent

    def has_parent(self):
        return self.parent is not None

    @property
    def directories(self):
        dirs = list(self.dirs)
        if self.has_parent():
            dirs += self.parent.directories
        return dirs

    @staticmethod
    def _combine_path(names):
        return os.path.join(*names) if isinstance(names, (list, tuple)) else names

    def get_template(self, template_name, template_factory):
        if template_name in self.template_cache:
            return self.template_cache[template_name]

        path = self._get_template_path(template_name)
        if path is not None:
            template = template_factory(path)
            self.template_cache[path] = template
            return template

        if self.parent is not None:
            return self.parent.get_template(template_name, template_factory)

        return None

    def _get_template_path(self, template_name):
        for template_dir in self.dirs:
            path = os.path.join(template_dir, template_name)
            if os.path.isfile(path):
                return path

        return None


class Composer:
    def __init__(self, app, rendering_adapter):
        from flask import request

        self.app = app
        self.components = []
        self.component_map = {}
        self.rendering_adapter = rendering_adapter
        self.default_context = {}
        self.add_context(app=self)
        self.current_component = None
        self.lookup = TemplatePathLookup(dirs=[(app.root_path, app.template_folder)])

        @app.before_request
        def before_request():
            self.current_component = self.component_map.get(request.blueprint, None)

        @app.after_request
        def after_request(response):
            self.current_component = None
            return response

    def add_context(self, **context):
        self.default_context.update(context)

    def register_component(self, component):
        self.app.register_blueprint(component.blueprint)
        self.components.append(component)
        self.component_map[component.name] = component
        component.register(self)

    def render_template(self, template_name, **context):
        return self.rendering_adapter.render_template(self.lookup, template_name, **self.get_context(context))

    def parts(self, name):
        parts = []
        cur_component = self.current_component
        try:
            for component in self.components:
                self.current_component = component
                parts += component.render_parts(name)
        finally:
            self.current_component = cur_component

        return parts

    def get_context(self, context):
        ctx = dict(self.default_context)
        ctx.update(context)
        return ctx

    def __getattr__(self, item):
        return getattr(self.app, item)


class Component:
    def __init__(self, name, import_name, parts_templates=('parts.html',)):
        from flask import Blueprint
        from flask.ext.composer.adapters import RenderingAdapter

        url_prefix = '/{0}/'.format(name)
        self.parts_templates = list(parts_templates)
        self.blueprint = Blueprint(name, import_name,
                                   static_folder='static',
                                   template_folder='templates',
                                   url_prefix=url_prefix)

        self.route = self.blueprint.route
        self.rendering_adapter = RenderingAdapter()
        self.container = None
        self.name = name
        self.lookup = TemplatePathLookup(dirs=[(self.blueprint.root_path, self.blueprint.template_folder)])

    def render_parts(self, name, **context):
        self._assert_registered()
        return self.rendering_adapter.render_parts(
            lookup=self.lookup,
            template_names=self.parts_templates,
            part_name=name,
            **self.container.get_context(context))

    def render_template(self, template_name, **context):
        self._assert_registered()
        return self.rendering_adapter.render_template(
            lookup=self.lookup,
            template_name=template_name,
            **self.container.get_context(context))

    def register(self, container):
        self._assert_not_registered()
        self.container = container
        self.rendering_adapter = container.rendering_adapter
        self.lookup.parent = container.lookup

    def _assert_not_registered(self):
        assert self.container is None, 'Plugin {0} is already registered into container'.format(self.name)

    def _assert_registered(self):
        assert self.container is not None, 'Plugin {0} is not registered into container'.format(self.name)
