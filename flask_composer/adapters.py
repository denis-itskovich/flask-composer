class RenderingAdapter(object):
    def render_template(self, lookup, template, *args, **kwargs):
        raise NotImplementedError()

    def render_parts(self, lookup, template_names, part_name, *args, **kwargs):
        raise NotImplementedError()


class MakoRenderingAdapter(RenderingAdapter):
    def __init__(self, app):
        import mako.lookup as lookup
        import mako as mako
        import mako.template as template

        self.mako = mako
        self.lookup = lookup
        self.template = template
        self.app = app

    def _create_template(self, lookup, path):
        factory = lambda path: self._create_template(lookup, path)

        class Lookup(self.lookup.TemplateLookup):
            def get_template(self, template_name):
                return lookup.get_template(template_name, factory)

            def adjust_uri(self, uri, relativeto):
                return lookup.adjust_uri(uri, relativeto)

        mako_lookup = Lookup(directories=lookup.directories)
        return self.template.Template(filename=path, lookup=mako_lookup)

    def _get_template(self, lookup, template_name):
        return lookup.get_template(template_name, lambda path: self._create_template(lookup, path))

    def render_template(self, lookup, template_name, *args, **kwargs):
        kwargs.update(self.app.jinja_env.globals)
        template = self._get_template(lookup, template_name)
        return template.render(*args, **kwargs) if template is not None else ''

    def render_parts(self, lookup, template_names, part_name, *args, **kwargs):
        kwargs.update(self.app.jinja_env.globals)
        rendered_parts = []
        for template_name in template_names:
            template = self._get_template(lookup, template_name)
            if template is None:
                continue
            if template.has_def(part_name):
                rendered_parts.append(template.get_def(part_name).render(*args, **kwargs))

        return rendered_parts
