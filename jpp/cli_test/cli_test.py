import os
import subprocess

import unittest

CURR_DIR = os.path.dirname(os.path.realpath(__file__))


class TestCli(unittest.TestCase):
    def getTestCaseNames(self):
        pass

    # Naming makes sure this test is run first. There's no reason to run the rest of the tests if installation failed
    def test00_installation(self):
        self.assertEqual(subprocess.call(['jpp', '--version']), 0, 'jpp not installed. Please run "pip install jpp" '
                                                                   'and try again.')

    def test_help(self):
        help_message = subprocess.check_output(['jpp', '-h'])
        self.assertRegex(help_message, '^usage:')

    def test_no_args(self):
        subprocess.check_call(['jpp'], cwd=CURR_DIR)

    def test_parse_specific_file(self):
        subprocess.check_call(['jpp', 'other.jpp'], cwd=CURR_DIR)

    def test_path_option(self):
        subprocess.check_call(['jpp', '--path', os.path.join(CURR_DIR, 'sub_path'), 'sub_other.jpp'], cwd=CURR_DIR)

    def test_compact_path(self):
        cmd_out = subprocess.check_output(['jpp', '--compact-print', 'compact_test.jpp'], cwd=CURR_DIR)
        # Make sure output is a one-liner
        self.assertEqual(cmd_out.count(b'\n'), 0)

    def test_user_input(self):
        subprocess.check_call(['jpp', '--user-input', '{"bar": "baz"}'], cwd=CURR_DIR)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
