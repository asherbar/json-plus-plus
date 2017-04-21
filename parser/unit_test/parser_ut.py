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

    def test_operations(self):
        source = """
        {
            "comparison": 1 < 3 < 8 | false & true,
            "bitwise": 1 & 2 ^ 3 | 4,
            "bit shift": 1 << 4 >> 2,
            "plus ints": 1+2+3,
            "plus string": "Hello, " + "World!",
            "minus": 1-2-3,
            "mul": 4 % 6 * 2 // 3 / 4,
            "mul strings": "a" * 3,
            "pow": 2 ** 8,
            "negative": -14,
            "invert": ~2,
            "parenthesis": (5 + 5) * (2 + 3),
            "precedent operation": 1 + 2**2 * -3 < 1 + -2**2 * -2
        }
        """
        self._verify(source, {'comparison': True, 'bitwise': 7, 'bit shift': 4, 'plus ints': 6,
                              'plus string': 'Hello, World!', 'minus': -4, 'mul': 0.5, 'pow': 256, 'mul strings': 'aaa',
                              'negative': -14, 'invert': -3, 'parenthesis': 50, 'precedent operation': True})
        source = """
        {
           "type mismatch": "1"*"2"
        }
        """
        self.assertRaises(TypeError, self.object_under_test.parse, source)

    def test_func(self):
        source = """
        {
            "abs": abs(1-2),
            "bool": bool(3.14) & bool(0)
        }
        """
        self._verify(source, {'abs': 1, 'bool': False})
