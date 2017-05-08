import argparse
import json
import os

from jpp.parser.grammar_def import GrammarDef

from jpp.parser.path_resolver import JPP_PATH, PATH_SPLITTER

DIRNAME = os.path.dirname(os.path.realpath(__file__))


yacc_default_init_args = {'debug': False, 'optimize': True, 'write_tables': False}
yacc_default_parse_args = {'tracking': True}


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Path to main JSON++ file', default='main.jpp')
    try:
        from __version__ import __version__
    except ImportError:
        __version__ = 'UNKNOWN: Unable to find __version__ file'
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
    parser.add_argument('-p', '--path', type=list, nargs='+', help='One or more path to add to JSON++ path', default=[])
    parser.add_argument('-c', '--compact-print', action='store_true',
                        help='If specified, will print the most compact version')
    parser.add_argument('-u', '--user-input', type=json.loads, help='Optional user input values', default={})
    return parser


def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()
    with open(args.file) as source_fp:
        source = source_fp.read()
    jpp_path_bk = os.environ.get(JPP_PATH, '')
    os.environ[JPP_PATH] = PATH_SPLITTER.join([DIRNAME] + args.path if args.path else [])
    if jpp_path_bk:
        os.environ[JPP_PATH] += PATH_SPLITTER + jpp_path_bk
    jpp_parser = GrammarDef(args.user_input).build(**yacc_default_init_args)
    json_args = {}
    if args.compact_print:
        json_args['separators'] = (',', ':')
    else:
        json_args['indent'] = 4
    jpp_parser.parse(source, **yacc_default_parse_args)
    print(json.dumps(jpp_parser.namespace, **json_args))


if __name__ == '__main__':
    main()
