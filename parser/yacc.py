import logging

import collections
import ply.yacc as yacc

from parser.lex import tokens


class _UndefinedReference:
    def __init__(self, name, line_no, line_pos):
        self.name = name
        self.line_no = line_no
        self.line_pos = line_pos

    def __str__(self):
        return '"{}" at line {}, column {}'.format(self.name, self.line_no, self.line_pos)


class _Reference:
    def __init__(self, ref_path):
        self.ref_path = ref_path


class GrammarDef:
    def __init__(self):
        self.yacc = None
        self._logger = logging.getLogger(self.__class__.__name__)
        self.namespace = {}
        self._dict_builder = {}
        self._list_builder = []
        self._dict_lookup_builder = []
        self._unresolved_refs = set()

        self.tokens = tokens

    def build(self, **yacc_params):
        self.yacc = yacc.yacc(module=self, **yacc_params)
        return self

    def parse(self, source, **yacc_parser_kwqrgs):
        if source:
            self.yacc.parse(source, **yacc_parser_kwqrgs)

    def p_start(self, _):
        """
        start : doc finish
        """

    def p_dict_doc(self, p):
        """
        doc : dict_def
        """
        self.namespace = p[1]

    def p_doc_with_imports(self, p):
        """
        doc : global_stmts SEMICOLON dict_def
        """
        self.namespace = p[3]

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
        self._dict_builder = {}

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
        ref : REF LBRAC dict_key RBRAC
        """
        # This won't work...
        p[0] = _Reference(p[3])
        self._unresolved_refs.add(p[3])

        # self._dict_lookup_builder = []
        # p[0] = self.namespace.get(p[3], _UndefinedReference(p[3], p.lineno(3), p.lexpos(3)))
        # if isinstance(p[0], _UndefinedReference):
        #     self._logger.error('Unknown reference: {}'.format(p[0]))
    #
    # def p_dict_lookup(self, p):
    #     """
    #     dict_lookup : LBRAC dict_key RBRAC
    #                 | LBRAC dict_key RBRAC dict_lookup
    #     """
    #     self._dict_lookup_builder.insert(0, p[2])

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
        self._list_builder = []

    def p_list_entries(self, p):
        """
        list_entries : dict_val
                     | dict_val COMMA
                     | dict_val COMMA list_entries
        """
        self._list_builder.insert(0, p[1])

    def p_integer_number(self, p):
        """
        number : INTEGER
        """
        p[0] = p[1]

    def p_float_number(self, p):
        """
        number : INTEGER DOT INTEGER
        """
        p[0] = float('{}.{}'.format(str(p[1]), p[3]))

    def p_finish(self, _):
        """
        finish :
        """
        self._resolve_references()

    def _resolve_references(self):
        unresolved_refs_num = len(self._unresolved_refs)
        while unresolved_refs_num:
            self._walk_iterable(self.namespace, self._resolve_single_reference)
            new_unresolved_refs_num = len(self._unresolved_refs)
            if unresolved_refs_num == new_unresolved_refs_num:
                self._logger.warning('Unable to resolve all references')
                break
            unresolved_refs_num = new_unresolved_refs_num

    @classmethod
    def _walk_iterable(cls, node, action_callable, _curr_path=None):
        if _curr_path is None:
            _curr_path = []
        if isinstance(node, dict):
            for key, val in node.items():
                _curr_path.append(key)
                action_callable(key, _curr_path)
                action_callable(val, _curr_path)
                cls._walk_iterable(val, action_callable, _curr_path)
        elif isinstance(node, list):
            for i, val in enumerate(node):
                _curr_path.append(i)
                action_callable(val, _curr_path)
                cls._walk_iterable(val, action_callable, _curr_path)
        if _curr_path:
            _curr_path.pop()

    def _resolve_single_reference(self, node, path_to_node):
        if isinstance(node, _Reference):
            referenced_value = self._get_indexed_value(self.namespace, [node.ref_path])
            if not isinstance(referenced_value, _Reference):
                self._set_indexed_value(self.namespace, path_to_node, referenced_value)
                self._unresolved_refs.remove(node.ref_path)

    @classmethod
    def _get_indexed_value(cls, indexed_obj, path_list):
        curr_level = indexed_obj
        for entry in path_list:
            curr_level = curr_level[entry]
        return curr_level

    @classmethod
    def _set_indexed_value(cls, indexed_obj, path_list, new_value):
        curr_level = indexed_obj
        for i in range(len(path_list) - 1):
            curr_level = curr_level[path_list[i]]
        curr_level[path_list[-1]] = new_value
