# -*- coding: utf-8 -*-

import os

from openfisca_core import columns, enumerations, reforms
from openfisca_france import entities
import numpy as np
import yaml


source_file_dir_name = os.path.dirname(os.path.abspath(__file__))
tabacs_yaml_file_path = os.path.join(source_file_dir_name, 'assets', 'tabacs.yaml')


# Functions for expressions


def apply_operator(yaml_input_variable, input_variable):
    # TODO Move this treatment in a Biryani validator when parsing the YAML file.
    operator, yaml_value = extract_operator_and_value(yaml_input_variable)
    return operator(input_variable, yaml_value)


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


# Functions for conditions matching


def match_conditions(yaml_variables_list, simulation, period):
    for yaml_variables in yaml_variables_list:
        yaml_input_variable_by_name = yaml_variables['input_variables']
        yaml_input_variables_name = sorted(yaml_input_variable_by_name)
        yaml_input_variables = [
            yaml_input_variable_by_name[yaml_input_variable_name]
            for yaml_input_variable_name in yaml_input_variables_name
            ]
        input_variables = [
            simulation.calculate(yaml_input_variable_name, period)
            for yaml_input_variable_name in yaml_input_variables_name
            ]
        conditions = (
            apply_operator(yaml_input_variable, input_variable)
            for input_variable, yaml_input_variable in zip(input_variables, yaml_input_variables)
            )
        if all(conditions):
            return yaml_variables
    return None


# Build reform function


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = u'douanes',
        name = u'Droits de douane, droits de consommation et TVA',
        reference = tax_benefit_system,
        )

    with open(tabacs_yaml_file_path, 'r') as tabacs_yaml_file:
        tabacs_yaml_variables_list = yaml.load(tabacs_yaml_file)
    yaml_variables_list = tabacs_yaml_variables_list
    # TODO Write a validator.

    def yaml_tree_variable_function(self, simulation, period):
        match = match_conditions(yaml_variables_list, simulation, period)
        result = self.zeros() + match['output_variables'][self.__class__.__name__] \
            if match is not None \
            else self.zeros()
        return period, result

    # Input variables

    class douanes_zone_provenance_produit(Reform.Variable):
        column = columns.EnumCol(enum = enumerations.Enum([u'Andorra', u'non_UE', u'UE']))
        entity_class = entities.Individus
        label = u'Zone de provenance du produit importé'

    class douanes_code_produit(Reform.Variable):
        column = columns.StrCol
        entity_class = entities.Individus
        label = u'Code du produit importé suivant la nomenclature des douanes'

    class douanes_quantite_produit(Reform.Variable):
        column = columns.IntCol
        entity_class = entities.Individus
        label = u'Quantité du produit importé'

    # Variables with formulas

    class taux_droits_douane_max(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.Individus
        function = yaml_tree_variable_function
        label = u'Taux de droits de douane sur un produit importé'

    class droits_consommation(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.Individus
        function = yaml_tree_variable_function
        label = u'Taux de droits de consommation sur un produit importé'

    class tva(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.Individus
        function = yaml_tree_variable_function
        label = u'Taux de TVA sur un produit importé'

    reform = Reform()
    return reform
