import logging


class _Reference:
    def __init__(self, ref_path):
        self.ref_path = ref_path


class ReferenceResolver:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.namespace = {}
        self._unresolved_refs = set()

    def create_reference(self, ref_path):
        self._unresolved_refs.add(ref_path)
        return _Reference(ref_path)

    def resolve_references(self):
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
