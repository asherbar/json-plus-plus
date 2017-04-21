class Expression:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value


class CompoundExpression(Expression):
    def __init__(self, operation, expression, expression2=None):
        super().__init__(None)
        self._operation = operation
        self._expression = expression
        self._expression2 = expression2

    @property
    def value(self):
        return self._operation(self._expression.value) if self._expression2 is None \
            else self._operation(self._expression.value, self._expression2.value)


class ReferencedExpression(Expression):
    def __init__(self, referenced_expression, reference_resolver):
        super().__init__(referenced_expression)
        self._reference_resolver = reference_resolver

    @property
    def _namespace(self):
        return self._reference_resolver.namespace

    @property
    def value(self):
        ret = self._namespace
        for key in self._value:
            ret = ret[key.value]
        return ret
