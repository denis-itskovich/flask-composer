from flask import Flask
import unittest
import json
import logging
from flask.ext.composer import Composer, Component
from flask.ext.composer.adapters import MakoRenderingAdapter


class ComposerTest(unittest.TestCase):
    def setUp(self):
        self.flask = Flask(__name__)
        self.log = logging.getLogger(self.id())

        self.container = Composer(self.flask, MakoRenderingAdapter(self.flask))

        import test_component_1
        import test_component_2

        self.component_1 = self.create_component('test_component_1', test_component_1.__name__)
        self.component_2 = self.create_component('test_component_2', test_component_2.__name__)

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

    def create_component(self, name, import_name):
        component = Component(name, import_name)

        @component.route('test')
        def component_test():
            return component.render_template('test.html')

        @component.route('test_with_include')
        def component_test_with_include():
            return component.render_template('test_with_include.html')

        self.container.register_component(component)
        return component

    def testRenderComponentTemplate(self):
        response = self.get_response('/test_component_1/test')
        self.assertTrue('<h1>test_component_1 test.html</h1>' in response)

    def testRenderGlobalTemplate(self):
        response = self.get_response('/test')
        self.assertTrue('<h1>global test.html</h1>' in response)

    def testRenderIncudeGlobalFromGlobalTakesGlobal(self):
        response = self.get_response('/test_with_include')
        self.assertTrue('<h1>global included.html</h1>' in response)

    def testRenderIncudeFromComponentTakesLocal(self):
        response = self.get_response('/test_component_1/test_with_include')
        self.assertTrue('<h1>local test_component_1 included.html</h1>' in response)

    def testRenderParts(self):
        response = self.get_response('/test_with_parts')
        self.assertTrue('<h1>test_with_parts.html</h1>' in response)
        self.assertTrue('<h1>test_component_1.test_part</h1>' in response)
        self.assertTrue('<h1>test_component_2.test_part</h1>' in response)

    def testGetModules(self):
        response = self.get_response('/components')

        resp_dic = json.loads(response)
        self.assertEqual(2, len(resp_dic))
        self.assertEqual('/test_component_1/static/js', resp_dic[0]['location'])
        self.assertEqual('test_component_1', resp_dic[0]['name'])
        self.assertTrue(resp_dic[0]['definition'] is not None)
        self.assertEqual('/test_component_2/static/js', resp_dic[1]['location'])
        self.assertEqual('test_component_2', resp_dic[1]['name'])
        self.assertTrue(resp_dic[1]['definition'] is None)

    def get_response(self, path):
        response = self.client.get(path)
        self.log.info("Response: %s", str(response.data))

        return str(response.data)

if __name__ == '__main__':
    unittest.main()
