import ply.lex as lex


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
    'BOOLEAN'
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


def t_INTEGER(t):
    r"""
    \d+
    """
    t.value = int(t.value)
    return t


def t_STRING_LITERAL(t):
    """
    "[^"\n]*"
    """
    t.value = t.value.strip('"')
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


def t_BOOLEAN(t):
    """
    true|false
    """
    t.value = t.value == 'true'
    return t


def t_newline(t):
    r"""
    \n+
    """
    t.lexer.lineno += len(t.value)


t_ignore = ' \t\n'


lexer = lex.lex(debug=False)
