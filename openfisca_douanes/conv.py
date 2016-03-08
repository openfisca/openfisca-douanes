import numbers

from biryani.baseconv import *  # noqa
from boolexp import Expression


item_to_singleton = make_item_to_singleton()


def str_to_expression(value, state = None):
    expression = value
    if 'value' not in value:
        operators = ('<', '<=', '>', '>=', '==')
        if all(operator not in value for operator in operators):
            if '"' not in value and "'" not in value:
                expression = u'"{}"'.format(expression)
            expression = u'== {}'.format(expression)
        expression = u'value {}'.format(expression)
    return Expression(expression), None


def make_validate_yaml_tree(categories_produits, variable_names):
    return pipe(
        test_isinstance(list),
        uniform_sequence(
            struct(
                {
                    'conditions': pipe(
                        test_isinstance(dict),
                        uniform_mapping(
                            pipe(
                                test_isinstance(basestring),
                                test_in(variable_names + ['categorie_produit']),
                                ),
                            pipe(
                                test_isinstance(basestring),
                                str_to_expression,
                                ),
                            ),
                        ),
                    'results': pipe(
                        test_isinstance(dict),
                        uniform_mapping(
                            test_in(variable_names),
                            test_isinstance(numbers.Real),
                            ),
                        ),
                    },
                ),
            ),
        )


validate_yaml_categories_produits = pipe(
    test_isinstance(list),
    uniform_sequence(
        pipe(
            test_isinstance(dict),
            uniform_mapping(
                test_isinstance(basestring),
                pipe(
                    test_isinstance(list),
                    uniform_sequence(
                        test_isinstance(basestring),
                        ),
                    ),
                ),
            ),
        ),
    )
