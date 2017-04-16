import json
import os
import unittest

from parser.yacc import GrammarDef


class ParserUnittest(unittest.TestCase):
    object_under_test = GrammarDef().build()

    def _verify(self, source, expected_namespace):
        self.object_under_test.parse(source)
        self.assertEqual(self.object_under_test.namespace, expected_namespace)

    def test_empty_doc(self):
        self._verify('', {})

    def test_simple_json(self):
        source = """
        {
            "standard json": {
                "hello": "world !",
                "list": [1, 2, 3],
                "number": 3.14,
                "bool": true
            }
        }
        """
        self._verify(source, json.loads(source))

    def test_full_json(self):
        with open(os.path.join(os.path.dirname(__file__), 'json_test.json')) as fp:
            source = fp.read()
        self._verify(source, json.loads(source))

    def test_local_ref(self):
        source = """
        {
            "foo": "bar",
            "ref": ref["foo"]
        }
        """
        self._verify(source, {'foo': 'bar', 'ref': 'bar'})

    def test_recursive_local_ref(self):
        source = """
        {
            "foo": "bar",
            "foobar": ref["foo"],
            "ref": ref["foobar"]
        }
        """
        self._verify(source, {'foo': 'bar', 'foobar': 'bar', 'ref': 'bar'})
        self._verify('', {})

    def test_comment(self):
        source = """
        \\ To be
        {
            "standard json": { \\ or not to be
                "hello": "world !",
                "list": [1, 2, 3],
                \\ that is
                "number": 3.14,
                "bool": true
            }
            \\ the
        }
        \\question
        """
        self._verify(source, {'standard json': {'hello': 'world !', 'list': [1, 2, 3], 'number': 3.14, 'bool': True}})
