import logging

from parser.expression import Expression


class _Reference:
    def __init__(self, ref_path):
        self.ref_path = ref_path
        self.resolved_value = None


class ReferenceResolver:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.namespace = {}
        self._unresolved_refs = set()
        self._ref_graph = {}

    def create_reference(self, ref_path):
        reference_obj = _Reference(ref_path)
        self._unresolved_refs.add(reference_obj)
        return reference_obj

    def resolve_references(self):
        need_resolve = False

        def resolve_value(node):
            if isinstance(node, list):
                ret = list(map(resolve_value, node))
            elif isinstance(node, dict):
                ret = {resolve_value(k): resolve_value(v) for k, v in node.items()}
            elif isinstance(node, Expression):
                try:
                    ret = node.value
                except KeyError:
                    ret = node
                else:
                    nonlocal did_resolve
                    did_resolve = True
            else:
                # value has been resolved already
                ret = node
            if isinstance(ret, Expression):
                nonlocal need_resolve
                need_resolve = True
            return ret

        self.namespace = {resolve_value(k): resolve_value(v) for k, v in self.namespace.items()}

        while need_resolve:
            need_resolve = False
            did_resolve = False
            self.namespace = {resolve_value(k): resolve_value(v) for k, v in self.namespace.items()}
            if need_resolve and not did_resolve:
                raise NameError('Unable to resove all references')

    def clear_namespace(self):
        self.namespace.clear()
