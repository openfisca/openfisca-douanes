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
    operator, yaml_input_variable = parse_expression(yaml_input_variable)
    return operator(input_variable, yaml_input_variable)


def is_expression(value):
    operators = ('<', '>', '<=', '>=')
    return isinstance(value, basestring) and any(operator in value for operator in operators)


def parse_expression(value):
    if is_expression(value):
        operator_str, value = value.split(' ')
        operator = {
            '<': np.less,
            '<=': np.less_equal,
            '>': np.greater,
            '>=': np.greater_equal,
            }[operator_str]
        value = int(value)
    else:
        operator = np.equal
    return operator, value


# Functions for conditions matching


def match_conditions(simulation, period, input_variables_and_values_list, output_variable_name):
    # TODO Cache the result because many variables may call this function with different `output_variable_name`.
    for input_variables_and_values in input_variables_and_values_list:
        yaml_input_variables_by_name = input_variables_and_values['input_variables']
        sorted_yaml_input_variables_name = sorted(yaml_input_variables_by_name)
        yaml_input_variables = [
            yaml_input_variables_by_name[yaml_input_variable_name]
            for yaml_input_variable_name in sorted_yaml_input_variables_name
            ]
        input_variables = [
            simulation.calculate(yaml_input_variable_name, period)
            for yaml_input_variable_name in sorted_yaml_input_variables_name
            ]
        conditions = (
            apply_operator(yaml_input_variable, input_variable)
            for input_variable, yaml_input_variable in zip(input_variables, yaml_input_variables)
            )
        if all(conditions):
            return input_variables_and_values['output_variables'][output_variable_name]
    return None


# Build reform function


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = u'douanes',
        name = u'Droits de douane, droits de consommation et TVA',
        reference = tax_benefit_system,
        )

    with open(tabacs_yaml_file_path, 'r') as tabacs_yaml_file:
        tabacs_input_variables_and_values_list = yaml.load(tabacs_yaml_file)
    # TODO Write a validator.

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

    class droits_douane_rate_max(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.Individus
        label = u'Taux de droits de douane sur un produit importé'

        def function(self, simulation, period):
            yaml_droits_douane_rate_max = match_conditions(
                input_variables_and_values_list = tabacs_input_variables_and_values_list,
                output_variable_name = 'droits_douane_rate_max',
                period = period,
                simulation = simulation,
                )
            result = self.zeros() + yaml_droits_douane_rate_max \
                if yaml_droits_douane_rate_max is not None \
                else self.zeros()
            return period, result

    class droits_consommation(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.Individus
        label = u'Taux de droits de consommation sur un produit importé'

        def function(self, simulation, period):
            yaml_droits_consommation = match_conditions(
                input_variables_and_values_list = tabacs_input_variables_and_values_list,
                output_variable_name = 'droits_consommation',
                period = period,
                simulation = simulation,
                )
            result = self.zeros() + yaml_droits_consommation \
                if yaml_droits_consommation is not None \
                else self.zeros()
            return period, result

    class tva(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.Individus
        label = u'Taux de TVA sur un produit importé'

        def function(self, simulation, period):
            yaml_tva = match_conditions(
                input_variables_and_values_list = tabacs_input_variables_and_values_list,
                output_variable_name = 'tva',
                period = period,
                simulation = simulation,
                )
            result = self.zeros() + yaml_tva \
                if yaml_tva is not None \
                else self.zeros()
            return period, result

    reform = Reform()
    return reform
