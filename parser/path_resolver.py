import os

PATH_SPLITTER = ';'

JPP_PATH = 'JPP_PATH'


class PathResolver:
    def __init__(self, ad_hoc_paths=()):
        env_paths = os.getenv(JPP_PATH, '').split(PATH_SPLITTER)
        env_paths.extend(ad_hoc_paths)
        self._search_paths = env_paths

    def resolve_path(self, dotted_path):
        for path in self._search_paths:
            found_path = self._find_path(path, dotted_path)
            if found_path is not None:
                return os.path.join(path, found_path)
        raise ImportError('Unable to find {}'.format(dotted_path))

    def _find_path(self, root, relative_dotted_path):
        path_to_dotted = os.path.join(root, relative_dotted_path.replace('.', os.path.sep) + '.jpp')
        if os.path.exists(path_to_dotted):
            return path_to_dotted

