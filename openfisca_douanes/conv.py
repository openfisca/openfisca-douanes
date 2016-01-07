import numbers

from biryani.baseconv import *  # noqa
import numpy as np


def extract_operator_and_value(value):
    operator_by_symbol = {
        '<': np.less,
        '<=': np.less_equal,
        '>': np.greater,
        '>=': np.greater_equal,
        }
    operators = operator_by_symbol.keys()
    if isinstance(value, basestring) and any(operator in value for operator in operators):
        operator_str, value = value.split(' ')
        operator = operator_by_symbol[operator_str]
        value = int(value)
    else:
        operator = np.equal
    return operator, value


validate_yaml_blocks = uniform_sequence(
    struct(
        {
            'conditions': uniform_mapping(
                noop,  # The variable name is not validated
                function(extract_operator_and_value),
                ),
            'results': uniform_mapping(
                noop,  # The variable name is not validated
                test_isinstance(numbers.Real),
                ),
            },
        ),
    )
