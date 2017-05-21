import argparse
import json
import os

import pkg_resources
import sys

from jpp.parser.grammar_def import GrammarDef
from jpp.parser.path_resolver import JPP_PATH, PATH_SPLITTER


yacc_default_init_args = {'debug': False, 'optimize': True, 'write_tables': False}
yacc_default_parse_args = {'tracking': True}


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Path to main JSON++ file', default='main.jpp', nargs='?')
    try:
        version = pkg_resources.require('jpp')[0].version
    except pkg_resources.DistributionNotFound:
        version = 'dev'
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(version))
    parser.add_argument('-p', '--path', type=json.loads, help='One or more path to add to JSON++ path', default=[])
    parser.add_argument('-c', '--compact-print', action='store_true',
                        help='If specified, will print the most compact version')
    parser.add_argument('-u', '--user-input', type=json.loads, help='Optional user input values', default={})
    parser.add_argument('-l', '--loose-mode', action='store_true',
                        help='If specified, unresolved nodes will be ignored')
    return parser


def main(cli_args=None, out_file_object=sys.stdout):
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args(cli_args)
    try:
        with open(args.file) as source_fp:
            source = source_fp.read()
    except FileNotFoundError as e:
        sys.stderr.write('{}\n'.format(str(e)))
        arg_parser.print_usage()
        sys.exit(e.errno)
    jpp_path_bk = os.environ.get(JPP_PATH, '')
    os.environ[JPP_PATH] = PATH_SPLITTER.join([os.getcwd()] + (args.path if args.path else []))
    if jpp_path_bk:
        os.environ[JPP_PATH] += PATH_SPLITTER + jpp_path_bk
    jpp_parser = GrammarDef(args.user_input, args.loose_mode).build(**yacc_default_init_args)
    json_args = {}
    if args.compact_print:
        json_args['separators'] = (',', ':')
    else:
        json_args['indent'] = 4
    jpp_parser.parse(source, **yacc_default_parse_args)
    out_file_object.write(json.dumps(jpp_parser.namespace, **json_args))


if __name__ == '__main__':
    main()
