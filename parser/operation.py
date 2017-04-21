import operator


class Operation:
    _name_to_func = {
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
        '>=': operator.ge,
        '>': operator.gt,
        'not': operator.not_,
        'bool': operator.truth,
        'abs': operator.abs,
        '+': operator.add,
        '&': operator.and_,
        '//': operator.floordiv,
        '~': operator.inv,
        '<<': operator.lshift,
        '%': operator.mod,
        '*': operator.mul,
        '|': operator.or_,
        '**': operator.pow,
        '>>': operator.rshift,
        '/': operator.truediv,
        '^': operator.xor,
    }

    def __init__(self, name, func=None):
        self._name = name
        self._func = func if func is not None else self._name_to_func[name]

    def __call__(self, arg1, arg2=None):
        return self._func(arg1) if arg2 is None else self._func(arg1, arg2)
