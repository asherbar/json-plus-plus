import logging

import collections
import ply.yacc as yacc

from parser.expression import ReferencedExpression
from parser.lex import tokens
from parser.reference_resolver import ReferenceResolver


class _UndefinedReference:
    def __init__(self, name, line_no, line_pos):
        self.name = name
        self.line_no = line_no
        self.line_pos = line_pos

    def __str__(self):
        return '"{}" at line {}, column {}'.format(self.name, self.line_no, self.line_pos)


class GrammarDef:
    def __init__(self):
        self.yacc = None
        self._logger = logging.getLogger(self.__class__.__name__)
        self._reference_resolver = ReferenceResolver()
        self._dict_builder = {}
        self._list_builder = collections.deque()
        self._lookup_builder = collections.deque()
        self.tokens = tokens

    def build(self, **yacc_params):
        self.yacc = yacc.yacc(module=self, **yacc_params)
        return self

    def parse(self, source, **yacc_parser_kwqrgs):
        if source:
            self.yacc.parse(source, **yacc_parser_kwqrgs)

    @property
    def namespace(self):
        return self._reference_resolver.namespace

    def clear_namespace(self):
        self._reference_resolver.clear_namespace()

    def p_start(self, _):
        """
        start : doc post_parsing
        """

    def p_dict_doc(self, p):
        """
        doc : dict_def
        """
        self._reference_resolver.namespace = p[1]

    def p_doc_with_imports(self, p):
        """
        doc : global_stmts SEMICOLON dict_def
        """
        self._reference_resolver.namespace = p[3]

    def p_global_stmts(self, p):
        """
        global_stmts : global_stmt SEMICOLON
                     | global_stmt SEMICOLON global_stmts
        """

    def p_global_stmt(self, p):
        """
        global_stmt : import_stmt
        """

    def p_import_stmt(self, p):
        """
        import_stmt : IMPORT dotted_name
        """

    def p_dotted_name(self, p):
        """
        dotted_name : NAME
                    | NAME DOT dotted_name
        """

    def p_dict_def(self, p):
        """
        dict_def : empty_dict_def
                 | non_empty_dict_def
        """
        p[0] = p[1]

    def p_empty_dict_def(self, p):
        """
        empty_dict_def : LCURL RCURL
        """
        p[0] = {}

    def p_non_empty_dict_def(self, p):
        """
        non_empty_dict_def : LCURL dict_entries RCURL
        """
        p[0] = dict(self._dict_builder)
        self._dict_builder.clear()

    def p_dict_entries(self, p):
        """
        dict_entries : dict_entry
                     | dict_entry COMMA
                     | dict_entry COMMA dict_entries
        """
        self._dict_builder[p[1][0]] = p[1][1]

    def p_dict_entry(self, p):
        """
        dict_entry : dict_key COLON dict_val
        """
        p[0] = (p[1], p[3])

    def p_dict_key(self, p):
        """
        dict_key : STRING_LITERAL
                 | BOOLEAN
                 | number
                 | ref
        """
        if not isinstance(p[1], collections.Hashable):
            self._logger.error('Unhashable dict key: {}, at line {}, column {}'.format(p[1], p.lineno(3), p.lexpos(3)))
        p[0] = p[1]

    def p_ref(self, p):
        """
        ref : REF lookup
        """
        p[0] = ReferencedExpression(list(self._lookup_builder), self._reference_resolver)
        self._lookup_builder.clear()

    def p_lookup(self, p):
        """
        lookup : LBRAC dict_key RBRAC
               | LBRAC dict_key RBRAC lookup
        """
        self._lookup_builder.appendleft(p[2])

    def p_dict_val(self, p):
        """
        dict_val : STRING_LITERAL
                 | BOOLEAN
                 | number
                 | ref
                 | dict_def
                 | list_def
        """
        p[0] = p[1]

    def p_list_def(self, p):
        """
        list_def : LBRAC RBRAC
                 | LBRAC list_entries RBRAC
        """
        p[0] = list(self._list_builder)
        self._list_builder.clear()

    def p_list_entries(self, p):
        """
        list_entries : dict_val
                     | dict_val COMMA
                     | dict_val COMMA list_entries
        """
        self._list_builder.appendleft(p[1])

    def p_integer_number(self, p):
        """
        number : INTEGER
        """
        p[0] = p[1]

    def p_float_number(self, p):
        """
        number : INTEGER DOT INTEGER
        """
        p[0] = float('{}.{}'.format(str(p[1].value), p[3].value))

    def p_finish(self, _):
        """
        post_parsing :
        """
        self._resolve_references()

    def _resolve_references(self):
        self._reference_resolver.resolve_references()
