
import unittest

from flask import Flask
from flask.ext.plugins import PluginManager, PluginError, get_plugins_list, \
    get_plugin


class InitializationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

    def test_init_app(self):
        plugin_manager = PluginManager()
        plugin_manager.init_app(self.app)

        self.assertIsInstance(plugin_manager, PluginManager)

    def test_class_init(self):
        plugin_manager = PluginManager(self.app)
        self.assertIsInstance(plugin_manager, PluginManager)


class PluginManagerTests(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.plugin_manager = PluginManager()
        self.plugin_manager.init_app(self.app)

    def test_find_plugins(self):
        found_plugins = self.plugin_manager.find_plugins()
        self.assertEqual(len(found_plugins), 3)
        expected_plugins = ['TestOnePlugin', 'TestTwoPlugin', 'TestThreePlugin']
        self.assertEquals(sorted(found_plugins), sorted(expected_plugins))

    def test_load_plugins(self):
        self.plugin_manager._plugins = None
        self.assertEquals(self.plugin_manager._plugins, None)

        self.plugin_manager.load_plugins()

        self.assertEquals(
            sorted(self.plugin_manager.plugins.keys()), ["test1", "test2"]
        )

        self.assertEquals(
            sorted(self.plugin_manager.all_plugins.keys()),
            ["test1", "test2", "test3"]
        )


class PluginManagerGetPlugins(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.plugin_manager = PluginManager()
        self.plugin_manager.init_app(self.app)

    def test_get_plugins_list(self):
        with self.app.test_request_context():
            plugins = get_plugins_list()

        self.assertEquals(
            set(plugins),
            set(self.plugin_manager.plugins.values())
        )

    def test_get_plugin(self):
        with self.app.test_request_context():
            plugin = get_plugin("test1")

        self.assertEquals(plugin, self.plugin_manager.plugins["test1"])


class PluginManagerOtherDirectoryTests(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.plugin_manager = PluginManager()

    def test_wrong_plugin(self):
        # should raise an exception because the plugin in the "plugs" folder
        # have set the __plugin__ variable not correctly.
        with self.assertRaises(PluginError):
            self.plugin_manager.init_app(self.app, plugin_folder="plugs")


class PluginManagerOnePluginTests(unittest.TestCase):
    """Tests the plugin.setup(), plugin.enabled()... methods"""
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.plugin_manager = PluginManager()
        self.plugin_manager.init_app(self.app)
        self.plugin_manager.load_plugins()

    def test_plugin_setup(self):
        plugin = self.plugin_manager.plugins["test1"]
        plugin.setup()
        self.assertTrue(plugin.setup_called)

    def test_plugin_install(self):
        plugin = self.plugin_manager.plugins["test1"]
        plugin.install()
        self.assertTrue(plugin.install_called)

    def test_plugin_uninstall(self):
        plugin = self.plugin_manager.plugins["test1"]
        plugin.uninstall()
        self.assertTrue(plugin.uninstall_called)


class PluginManagerManagementMethodsTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.plugin_manager = PluginManager()
        self.plugin_manager.init_app(self.app)

        # Call load_plugins to reload them without calling setup_plugins()
        self.plugin_manager.load_plugins()

    def test_setup_plugins(self):
        plugin = self.plugin_manager.plugins["test1"]
        self.assertFalse(plugin.setup_called)

        self.plugin_manager.setup_plugins()

        self.assertTrue(plugin.setup_called)

    def test_install_plugins(self):
        plugin = self.plugin_manager.plugins["test1"]
        self.assertFalse(plugin.install_called)

        self.plugin_manager.install_plugins()

        self.assertTrue(plugin.install_called)

    def test_uninstall_plugins(self):
        plugin = self.plugin_manager.plugins["test1"]
        self.assertFalse(plugin.uninstall_called)

        self.plugin_manager.uninstall_plugins()

        self.assertTrue(plugin.uninstall_called)
