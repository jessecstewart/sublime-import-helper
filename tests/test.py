import sublime
import sys
from unittest import TestCase
import_helper = sys.modules['ImportHelper.import_helper']
from time import sleep

# window.run_command('update_imports')

class TestUpdateImports(TestCase):
    
    def setUp(self):
        self.window = sublime.active_window()
        self.window.run_command('update_imports')
    
    def test_check_node_modules(self):
        sleep(4)
        self.assertNotEqual(len(import_helper.node_modules), 0)

    def test_check_source_modules(self):
        self.assertNotEqual(len(import_helper.source_modules), 0)

    def test_exclude_should_work(self):
        ignored = [item for item in import_helper.source_modules if 'ignored' in item['filepath']]
        self.assertEqual(len(ignored), 0)

class TestUtilFunctions(TestCase):

    def test_debug_disabled(self):
        self.assertFalse(import_helper.DEBUG)

    def test_run_path_should_point_to_debug_version(self):
        run_path = import_helper.RUN_PATH
        self.assertIn('backend_run', run_path)

    def test_unixify(self):
        unixify = import_helper.unixify
        _ = '\\local\\some\\file'
        self.assertTrue(unixify(_) == '/local/some/file')
        
    def test_unixify_ts(self):
        unixify = import_helper.unixify
        _ = 'some\\file.ts'
        self.assertTrue(unixify(_) == 'some/file')
        
    def test_unixify_js(self):
        unixify = import_helper.unixify
        _ = 'some\\file.js'
        self.assertTrue(unixify(_) == 'some/file')

    def test_is_excluded_file(self):
        is_excluded_file = import_helper.is_excluded_file
        self.assertTrue(is_excluded_file('dir/file1.ts', ['*.ts']))
        self.assertTrue(is_excluded_file('dir1/file1.ts', ['dir1']))

class TestExample(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def setText(self, string):
        self.view.run_command("insert", {"characters": string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def test_smoke(self):
        self.assertTrue(True)
        
    # def test_hello_world(self):
    #     self.view.run_command("hello_world")
    #     first_row = self.getRow(0)
    #     self.assertEqual(first_row, "hello world")