import os
import shutil
import subprocess

import unittest
from collections import namedtuple

CURR_DIR = os.path.dirname(os.path.realpath(__file__))


class TestCli(unittest.TestCase):
    TMP_TEST_FILES = os.path.join(CURR_DIR, '__tmp__')

    @classmethod
    def setUpClass(cls):
        FileDef = namedtuple('FileDef', ('name', 'contents', 'sub_path'))
        required_files = (
            FileDef('compact_test.jpp', '{\n"many": 1, \n"lines": 2\n}', ''),
            FileDef('main.jpp', '', ''),
            FileDef('other.jpp', '', ''),
            FileDef('user_input_test.jpp', '{"foo": user_input["bar"]}', ''),
            FileDef('sub_other.jpp', '', 'sub_path'),
        )
        os.mkdir(cls.TMP_TEST_FILES)
        for file_def in required_files:
            if file_def.sub_path:
                os.mkdir(os.path.join(cls.TMP_TEST_FILES, file_def.sub_path))
                file_path = os.path.join(cls.TMP_TEST_FILES, file_def.sub_path, file_def.name)
            else:
                file_path = os.path.join(cls.TMP_TEST_FILES, file_def.name)
            with open(file_path, 'w') as fp:
                fp.write(file_def.contents)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.TMP_TEST_FILES)

    # Naming makes sure this test is run first. If --failfast option is specified the rest of the tests will no run
    def test00_installation(self):
        try:
            subprocess.call(['jpp', '--version'])
        except FileNotFoundError:
            installed = False
        else:
            installed = True
        if not installed:
            self.fail('jpp not installed. Please run "pip install jpp" and try again.')

    def test_help(self):
        help_message = subprocess.check_output(['jpp', '-h'])
        self.assertRegex(help_message, '^usage:')

    def test_no_args(self):
        subprocess.check_call(['jpp'], cwd=self.TMP_TEST_FILES)

    def test_parse_specific_file(self):
        subprocess.check_call(['jpp', 'other.jpp'], cwd=self.TMP_TEST_FILES)

    def test_path_option(self):
        subprocess.check_call(['jpp', '--path', os.path.join(CURR_DIR, 'sub_path'), 'sub_other.jpp'],
                              cwd=self.TMP_TEST_FILES)

    def test_compact_path(self):
        cmd_out = subprocess.check_output(['jpp', '--compact-print', 'compact_test.jpp'], cwd=self.TMP_TEST_FILES)
        # Make sure output is a one-liner
        self.assertEqual(cmd_out.count(b'\n'), 0)

    def test_user_input(self):
        subprocess.check_call(['jpp', '--user-input', '{"bar": "baz"}', 'user_input_test.jpp'], cwd=self.TMP_TEST_FILES)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
