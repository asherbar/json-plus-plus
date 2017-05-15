import os
import shutil
import unittest
from collections import namedtuple
from io import StringIO

from jpp.cli import main as cli_entry_point

CURR_DIR = os.path.dirname(os.path.realpath(__file__))


class TestCli(unittest.TestCase):
    TMP_TEST_FILES = os.path.join(CURR_DIR, '__tmp__')
    _dir_bk = None

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

        cls._dir_bk = os.getcwd()
        os.chdir(os.path.join(cls.TMP_TEST_FILES))

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._dir_bk)
        shutil.rmtree(cls.TMP_TEST_FILES)

    def test_version(self):
        cli_entry_point(['--version'])

    def test_help(self):
        out_file_object = StringIO()
        cli_entry_point(['jpp', '-h'], out_file_object)
        self.assertRegex(out_file_object.read(), b'^usage:')

    def test_no_args(self):
        out_file_object = StringIO()
        cli_entry_point(['jpp'], out_file_object)
        self.assertEqual(out_file_object.read(), '{}')

    def test_parse_specific_file(self):
        out_file_object = StringIO()
        cli_entry_point(['jpp', 'other.jpp'], out_file_object)
        self.assertEqual(out_file_object.read(), '{}')

    def test_path_option(self):
        out_file_object = StringIO()
        cli_entry_point(['jpp', '--path', os.path.join(CURR_DIR, 'sub_path'), 'sub_other.jpp'], out_file_object)
        self.assertEqual(out_file_object.read(), '{}')

    def test_compact_path(self):
        out_file_object = StringIO()
        cli_entry_point(['jpp', '--compact-print', 'compact_test.jpp'], out_file_object)
        self.assertEqual(out_file_object.read(), '{}')
        # Make sure output is a one-liner at most
        self.assertLessEqual(out_file_object.read()(b'\n'), 1)

    def test_user_input(self):
        out_file_object = StringIO()
        cli_entry_point(['jpp', '--compact-print', '--user-input', '{"bar": "baz"}', 'user_input_test.jpp'],
                        out_file_object)
        self.assertEqual(out_file_object.read(), '{"foo": "baz"}\n')


def main():
    unittest.main()

if __name__ == '__main__':
    main()
