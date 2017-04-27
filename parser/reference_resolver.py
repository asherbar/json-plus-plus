import logging

from parser.expression import Expression


class NamespaceResolver:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.namespace = {}
        self._unresolved_refs = set()
        self._ref_graph = {}

    def resolve_references(self):
        need_resolve = True

        def resolve_value(node):
            nonlocal need_resolve
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
                    if isinstance(ret, (list, dict)):
                        need_resolve = True
            else:
                # value has been resolved already
                ret = node
            if isinstance(ret, Expression):
                need_resolve = True
            return ret

        while need_resolve:
            need_resolve = False
            did_resolve = False
            self.namespace = {resolve_value(k): resolve_value(v) for k, v in self.namespace.items()}
            if need_resolve and not did_resolve:
                raise NameError('Unable to resolve all references')

    def clear_namespace(self):
        self.namespace.clear()
