from parser.path_resolver import PathResolver


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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._current_importing_dependencies.clear()
        self._current_importing_dependencies_path.clear()

    def _resolve_namespace(self, dotted_name):
        path = self._path_resolver.resolve_path(dotted_name)
        with open(path) as fp:
            source = fp.read()
        from parser.grammar_def import GrammarDef
        grammar_def = GrammarDef().build()
        grammar_def.parse(source)
        return grammar_def.namespace


def get_importer():
    try:
        return globals()['_importer']
    except KeyError:
        pass
    globals()['_importer'] = _Importer()
    return globals()['_importer']
