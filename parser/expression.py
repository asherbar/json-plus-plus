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
        return self._operation(self._expression) if self._expression2 is None \
            else self._operation(self._expression, self._expression2)


class ReferencedExpression(Expression):
    def __init__(self, referenced_expression, reference_resolver):
        super().__init__(referenced_expression)
        self._reference_resolver = reference_resolver

    @property
    def _namespace(self):
        return self._reference_resolver.namespace

    @property
    def value(self):
        return self._namespace[self._value.value]


class Operation:
    pass


class OperationPlus(Operation):
    def __call__(self, exp1, exp2):
        return exp1.value + exp2.value
