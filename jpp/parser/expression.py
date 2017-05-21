class UnableToResolveValue(KeyError):
    pass


class Expression:
    @property
    def value(self):
        raise NotImplementedError()

    def __repr__(self):
        return str(self)


class SimpleExpression(Expression):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class CompoundExpression(Expression):
    def __init__(self, operation, expression, expression2=None):
        super().__init__()
        self._operation = operation
        self._expression = expression
        self._expression2 = expression2

    @property
    def value(self):
        return self._operation(self._expression.value) if self._expression2 is None \
            else self._operation(self._expression.value, self._expression2.value)

    def __str__(self):
        ret = '{}{}'.format(self._operation, self._expression)
        if self._expression2 is not None:
            ret += str(self._expression2)
        return ret


class LocalReferencedExpression(Expression):
    def __init__(self, referenced_expression, reference_resolver):
        super().__init__()
        self._referenced_expression = referenced_expression
        self._reference_resolver = reference_resolver

    @property
    def _namespace(self):
        return self._reference_resolver.namespace

    @property
    def value(self):
        ret = self._namespace
        for key in self._referenced_expression:
            ret = ret[key.value]
        return ret

    def __str__(self):
        return 'Local: {}'.format(self._referenced_expression)


class ImportedReferencedExpression(LocalReferencedExpression):
    def __init__(self, referenced_expression, imports):
        super().__init__(referenced_expression, None)
        self._imports = imports

    @property
    def _namespace(self):
        return self._imports

    def __str__(self):
        return 'Imported: {}'.format(self._referenced_expression)


class UserInputReferencedExpression(LocalReferencedExpression):
    def __init__(self, referenced_expression, user_inputs):
        super().__init__(referenced_expression, None)
        self._user_inputs = user_inputs

    @property
    def _namespace(self):
        return self._user_inputs

    def __str__(self):
        return 'User: {}'.format(self._reference_resolver)


class ExtendsExpression(Expression):
    def __init__(self, base_expression, extended_value):
        super().__init__()
        self._base_expression = base_expression
        self._extended_value = extended_value
        if not isinstance(self._extended_value, dict):
            raise TypeError('Type {} cannot be extended (must be of type dict)'.format(type(self._extended_value)))

    @property
    def value(self):
        base_dict = self._base_expression.value
        if not isinstance(base_dict, dict):
            raise TypeError('Unable to extend type {} (must be of type dict)'.format(type(base_dict)))
        base_dict = dict(base_dict)
        self._extended_value = {k.value if isinstance(k, Expression) else k: v for k, v in self._extended_value.items()}
        base_dict.update(self._extended_value)
        return base_dict

    def __str__(self):
        return '{} extends {}'.format(self._extended_value, self._base_expression)
