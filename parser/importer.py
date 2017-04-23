from parser.path_resolver import PathResolver
from parser.yacc import GrammarDef


class _Importer:
    def __init__(self):
        self._cache = {}
        self._current_importing_dependencies = set()
        self._current_importing_dependencies_path = []
        self._path_resolver = PathResolver()

    def import_namespace(self, dotted_name):
        try:
            return self._cache[dotted_name]
        except KeyError:
            pass

        if dotted_name in self._current_importing_dependencies:
            self._current_importing_dependencies_path.append(dotted_name)
            raise ImportError('Circular dependency: {}'.format(' --> '.join(self._current_importing_dependencies_path)))
        self._current_importing_dependencies_path.append(dotted_name)
        self._current_importing_dependencies.add(dotted_name)
        self._cache[dotted_name] = self._resolve_namespace(dotted_name)
        return self._cache[dotted_name]

    def _resolve_namespace(self, dotted_name):
        path = self._path_resolver.resolve_path(dotted_name)
        with open(path) as fp:
            source = fp.read()
        grammar_def = GrammarDef(self).build()
        grammar_def.parse(source)
        return grammar_def.namespace


def get_importer():
    try:
        return globals()['_importer']
    except KeyError:
        pass
    globals()['_importer'] = _Importer()
    return globals()['_importer']
