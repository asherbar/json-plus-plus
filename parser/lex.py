import operator

import ply.lex as lex

from parser.expression import Expression
from parser.operation import Operation

reserved = {
    'extends': 'EXTENDS',
    'import': 'IMPORT',
    'ref': 'REF'
}

NAME_TOK = 'NAME'

tokens = [
    'INTEGER',
    'STRING_LITERAL',
    'COLON',
    NAME_TOK,
    'COMMA',
    'LCURL',
    'RCURL',
    'LBRAC',
    'RBRAC',
    'LPAREN',
    'RPAREN',
    'DOT',
    'SEMICOLON',
    'BOOLEAN',
    'MINUS',
    'COMPARISON_OP',
    'PLUS',
    'MUL_OP',
    'BIT_SHIFT_OPS',
    'BITWISE_OPS',
    'INVERT',
    'POW',
    'FUNC',
]

tokens.extend(reserved.values())

t_DOT = r'\.'
t_LCURL = r'\{'
t_RCURL = r'\}'
t_COLON = r'\:'
t_LBRAC = r'\['
t_RBRAC = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = ','
t_SEMICOLON = ';'


def _create_operation_token(t):
    t.value = Operation(t.value)
    return t


def t_BIT_SHIFT_OPS(t):
    """
    <<|>>
    """
    return _create_operation_token(t)


def t_COMPARISON_OP(t):
    """
    <|<=|==|!=|>=
    """
    return _create_operation_token(t)


def t_BITWISE_OPS(t):
    r"""
    &|\^|\|
    """
    return _create_operation_token(t)


def t_PLUS(t):
    r"""
    \+
    """
    return _create_operation_token(t)


def t_MINUS(t):
    r"""
    -
    """
    t.value = Operation(t.value, operator.sub)
    return t


def t_POW(t):
    r"""
    \*\*
    """
    return _create_operation_token(t)


def t_MUL_OP(t):
    r"""
    \*|//|/|%
    """
    return _create_operation_token(t)


def t_INVERT(t):
    """
    ~
    """
    return _create_operation_token(t)


def t_FUNC(t):
    """
    bool|abs
    """
    return _create_operation_token(t)


def t_INTEGER(t):
    r"""
    \d+
    """
    t.value = Expression(int(t.value))
    return t


def t_STRING_LITERAL(t):
    """
    "[^"\n]*"
    """
    t.value = Expression(str(t.value).strip('"'))
    return t


def t_BOOLEAN(t):
    """
    true|false
    """
    t.value = Expression(t.value == 'true')
    return t


def t_NAME(t):
    """
    (?!true|false)[a-zA-Z_][a-zA-Z_0-9]*
    """
    t.type = reserved.get(t.value, NAME_TOK)  # Check for reserved words
    return t


def t_COMMENT(t):
    r"""
    \\.*
    """
    # No return value. Token discarded
    pass


def t_newline(t):
    r"""
    \n+
    """
    t.lexer.lineno += len(t.value)


t_ignore = ' \t\n'

lexer = lex.lex(debug=False)
