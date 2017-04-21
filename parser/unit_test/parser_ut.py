import json
import os
import unittest

from parser.yacc import GrammarDef


class ParserUnittest(unittest.TestCase):
    object_under_test = GrammarDef().build()

    def setUp(self):
        self.object_under_test.clear_namespace()

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

    def test_local_ref_of_ref(self):
        source = """
        {
            "foo": "bar",
            "bar": "foobar",
            "foobar": "hi",
            "ref1": ref[ref["foo"]],
            "nest": {
                "ref2": ref[ref[ref["foo"]]]
            }
        }
        """
        self._verify(source, {'foo': 'bar', 'bar': 'foobar', 'foobar': 'hi', 'ref1': 'foobar', 'nest': {'ref2': 'hi'}})

    def test_bad_ref(self):
        source = """
        {
            "foo": ref["bar"]
        }
        """
        self.assertRaises(NameError, self.object_under_test.parse, source)

    def test_ref_lookup_path(self):
        source = """
        {
            "foo": {"bar": {"foobar": [19, 84]}},
            "baz": ref["foo"]["bar"]["foobar"][1]
        }
        """
        self._verify(source, {'foo': {'bar': {'foobar': [19, 84]}}, 'baz': 84})

    def test_plus_operator(self):
        source = """
        {
            "plus int": 1+2,
            "plus float": 1.4 + 2.5,
            "plus string": "Hello, " + "World!",
            "plus ref": ref["plus int"] + 8,
            "uneven plus": 1+2+3,
            "even plus": 1+2+3+4,
            "int plus float": 1 + 2.5,
            1 + 3: 14 + 12
        }
        """
        self._verify(source, {'plus int': 3, 'plus float': 3.9, 'plus string': 'Hello, World!', 'plus ref': 11,
                              'uneven plus': 6, 'even plus': 10, 'int plus float': 3.5, 4: 26})
        source = """
        {
           "type mismatch": 1+"2"
        }
        """
        self.assertRaises(TypeError, self.object_under_test.parse, source)

    def test_minus_operator(self):
        source = """
        {
            "minus int": 1-2,
            "minus float": 1.4 - 2.5,
            "minus ref": ref["minus int"] - 8,
            "uneven minus": 1-2-3,
            "even minus": 1-2-3-4,
            "int minus float": 1 - 2.5,
            1 - 3: 14 - 12
        }
        """
        self._verify(source, {'minus int': -1, 'minus float': -1.1, 'minus ref': -9, 'uneven minus': -4,
                              'even minus': -8, 'int minus float': -1.5, -2: 2})
        source = """
        {
           "type mismatch": 1-"2"
        }
        """
        self.assertRaises(TypeError, self.object_under_test.parse, source)

    def test_mul_operator(self):
        source = """
        {
            "mul int": 1*2,
            "mul float": 1.4 * 2.5,
            "mul ref": ref["mul int"] * 8,
            "uneven mul": 1*2*3,
            "even mul": 1*2*3*4,
            "int mul float": 1 * 2.5,
            1 * 3: 14 * 12,
            "mul strings": "a" * 3
        }
        """
        self._verify(source, {'mul int': 2, 'mul float': 3.5, 'mul ref': 16, 'uneven mul': 6, 'even mul': 24,
                              'int mul float': 2.5, 3: 168, 'mul strings': 'aaa'})
        source = """
        {
           "type mismatch": "1"*"2"
        }
        """
        self.assertRaises(TypeError, self.object_under_test.parse, source)
