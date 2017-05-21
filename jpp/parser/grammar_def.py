import collections
import logging
import operator

import ply.yacc as yacc
from jpp.parser.importer import get_importer
from jpp.parser.lex import tokens, create_lexer
from jpp.parser.operation import Operation
from jpp.parser.reference_resolver import ReferenceResolver

from jpp.parser.expression import LocalReferencedExpression, CompoundExpression, SimpleExpression, \
    ImportedReferencedExpression, ExtendsExpression, UserInputReferencedExpression


class _UndefinedReference:
    def __init__(self, name, line_no, line_pos):
        self.name = name
        self.line_no = line_no
        self.line_pos = line_pos

    def __str__(self):
        return '"{}" at line {}, column {}'.format(self.name, self.line_no, self.line_pos)


# noinspection PyClassHasNoInit
class SyntaxErrorMsg(collections.namedtuple('SyntaxErrorMsg', ['source_line', 'line_no', 'pos_no'])):
    _MAX_SOURCE_LEN = 50

    def __str__(self):
        return 'Syntax Error at line {}:{}.\n{}'.format(self.line_no, self.pos_no, self._get_snipped_source_line())

    def _get_snipped_source_line(self):
        pos_delta = self._MAX_SOURCE_LEN // 2
        start = max(0, self.pos_no - pos_delta)
        end = self.pos_no + pos_delta
        ret = self.source_line[start:end]
        carrot_pos = pos_delta
        padding = '...'
        if start > 0:
            ret = padding + ret
            carrot_pos += len(padding)
        if end < len(self.source_line):
            ret += padding
        return '{}\n{}'.format(ret, ' '*(carrot_pos - 1) + '^')


class SyntaxErrorAtEof:
    def __str__(self):
        return 'Syntax Error: Unexpected end of file'


class GrammarDef:
    precedence = (
        ('left', 'COMPARISON_OP', 'BITWISE_OPS'),
        ('left', 'BIT_SHIFT_OPS'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL_OP'),
        ('left', 'POW'),
        ('right', 'UMINUS', 'INVERT'),  # Unary minus operator
    )

    def __init__(self, user_inputs=None, loose=False):
        self._user_inputs = {} if user_inputs is None else user_inputs
        self._imports = {}
        self.yacc = None
        self._logger = logging.getLogger(self.__class__.__name__)
        self._reference_resolver = ReferenceResolver(loose)
        self._dict_builder = {}
        self._list_builder = collections.deque()
        self._dotted_name_builder = collections.deque()
        self._curr_lookup_builder = collections.deque()
        self.tokens = tokens
        self._source = ''
        self._split_source = []

    def build(self, **yacc_params):
        self.yacc = yacc.yacc(module=self, **yacc_params)
        return self

    def parse(self, source, lexer=None, **yacc_parser_kwargs):
        if source:
            self._source = source
            self._split_source = source.split('\n')
            self.yacc.parse(source, lexer=create_lexer() if lexer is None else lexer, **yacc_parser_kwargs)

    @property
    def namespace(self):
        return self._reference_resolver.namespace

    @property
    def imports(self):
        return self._imports

    @property
    def user_inputs(self):
        return self._user_inputs

    def clear_namespace(self):
        self._reference_resolver.clear_namespace()

    def _get_source_line(self, line_no):
        return self._split_source[line_no]

    def p_error(self, p):
        if p:  # I.e., not EOF
            column_pos = self._get_column(p)-1
            err_msg = SyntaxErrorMsg(self._get_source_line(p.lineno-1), p.lineno, column_pos)
            log_msg = 'Syntax error at {}:{}'.format(p.lineno, column_pos)
        else:
            err_msg = SyntaxErrorAtEof()
            log_msg = 'Syntax error at EOF'
        self._logger.error(log_msg)
        raise SyntaxError(str(err_msg))


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
        doc : global_stmts dict_def
        """
        self._reference_resolver.namespace = p[2]

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
        dotted_name = '.'.join(self._dotted_name_builder)
        with get_importer() as importer:
            self._imports[dotted_name] = importer.import_namespace(dotted_name)
        self._imports[dotted_name.split('.')[-1]] = self._imports[dotted_name]
        self._dotted_name_builder.clear()

    def p_dotted_name(self, p):
        """
        dotted_name : NAME
                    | NAME DOT dotted_name
        """
        self._dotted_name_builder.appendleft(p[1])

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

    def p_extended_dict_entry(self, p):
        """
        dict_entry : dict_key EXTENDS dict_key COLON dict_def
        """
        p[0] = (p[1], ExtendsExpression(p[3], p[5]))

    def p_dict_key(self, p):
        """
        dict_key : expression
        """
        p[0] = p[1]

    def p_literal(self, p):
        """
        literal  : STRING_LITERAL
                 | BOOLEAN
                 | number
                 | ref
        """
        p[0] = p[1]

    def p_literal_expression(self, p):
        """
        expression : literal
        """
        p[0] = p[1]

    def p_enclosed_expression(self, p):
        """
        expression : LPAREN expression RPAREN
        """
        p[0] = p[2]

    def p_two_place_operation_expression(self, p):
        """
        expression : expression COMPARISON_OP expression
                   | expression BITWISE_OPS expression
                   | expression BIT_SHIFT_OPS expression
                   | expression PLUS expression
                   | expression MINUS expression
                   | expression MUL_OP expression
                   | expression POW expression
        """
        p[0] = CompoundExpression(p[2], p[1], p[3])

    def p_invert_expression(self, p):
        """
        expression : INVERT expression
        """
        p[0] = CompoundExpression(p[1], p[2])

    def p_negative_expression(self, p):
        """
        expression : MINUS expression %prec UMINUS
        """
        p[0] = CompoundExpression(Operation('-', operator.neg), p[2])

    def p_function_expression(self, p):
        """
        expression : FUNC LPAREN expression RPAREN
        """
        p[0] = CompoundExpression(p[1], p[3])

    def p_local_ref(self, p):
        """
        ref : LOCAL lookup
        """
        p[0] = LocalReferencedExpression(list(self._curr_lookup_builder), self._reference_resolver)
        self._curr_lookup_builder.clear()

    def p_imported_ref(self, p):
        """
        ref : IMPORTED lookup
        """
        p[0] = ImportedReferencedExpression(list(self._curr_lookup_builder), self._imports)
        self._curr_lookup_builder.clear()

    def p_user_input_ref(self, p):
        """
        ref : USER_INPUT lookup
        """
        p[0] = UserInputReferencedExpression(list(self._curr_lookup_builder), self._user_inputs)
        self._curr_lookup_builder.clear()

    def p_lookup(self, p):
        """
        lookup : LBRAC dict_key RBRAC
               | LBRAC dict_key RBRAC lookup
        """
        self._curr_lookup_builder.appendleft(p[2])

    def p_dict_val(self, p):
        """
        dict_val : dict_key
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
        p[0] = SimpleExpression(float('{}.{}'.format(str(p[1].value), p[3].value)))

    def p_finish(self, _):
        """
        post_parsing :
        """
        self._resolve_references()

    def _resolve_references(self):
        self._reference_resolver.resolve_references()

    def _get_column(self, token):
        last_cr = self._source.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column
