from flask import Flask

__author__ = 'Denis'

import unittest
from flask.ext.composer import composer


class PluginContainerTest(unittest.TestCase):
    def setUp(self):
        self.flask = Flask(__name__)

        self.container = composer.Composer(self.flask, composer.MakoRenderingAdapter(self.flask))

        import test_plugin_1
        import test_plugin_2

        self.plugin_1 = self.create_plugin('test_plugin_1', test_plugin_1.__name__)
        self.plugin_2 = self.create_plugin('test_plugin_2', test_plugin_2.__name__)

        @self.container.route('/test')
        def global_test():
            return self.container.render_template('test.html')

        @self.container.route('/test_with_parts')
        def test_with_parts():
            return self.container.render_template('test_with_parts.html')

        @self.container.route('/test_with_include')
        def test_with_include():
            return self.container.render_template('test_with_include.html')

        from flask.ext.composer import helpers
        self.container.add_context(helpers=helpers.Helper(self.container))

        self.flask.config['TESTING'] = True
        self.client = self.flask.test_client()

    def create_plugin(self, name, import_name):
        plugin = composer.Component(name, import_name)

        @plugin.route('test')
        def plugin_test():
            return plugin.render_template('test.html')

        @plugin.route('test_with_include')
        def plugin_test_with_include():
            return plugin.render_template('test_with_include.html')

        self.container.register_plugin(plugin)
        return plugin

    def testRenderPluginTemplate(self):
        response = self.client.get('/test_plugin_1/test')
        self.assertTrue('<h1>test_plugin_1 test.html</h1>' in response.data)

    def testRenderGlobalTemplate(self):
        response = self.client.get('/test')
        self.assertTrue('<h1>global test.html</h1>' in response.data)

    def testRenderIncudeGlobalFromGlobalTakesGlobal(self):
        response = self.client.get('/test_with_include')
        self.assertTrue('<h1>global included.html</h1>' in response.data)

    def testRenderIncudeFromPluginTakesLocal(self):
        response = self.client.get('/test_plugin_1/test_with_include')
        self.assertTrue('<h1>local test_plugin_1 included.html</h1>' in response.data)

    def testRenderParts(self):
        response = self.client.get('/test_with_parts')
        self.assertTrue('<h1>test_with_parts.html</h1>' in response.data)
        self.assertTrue('<h1>test_plugin_1.test_part</h1>' in response.data)
        self.assertTrue('<h1>test_plugin_2.test_part</h1>' in response.data)
