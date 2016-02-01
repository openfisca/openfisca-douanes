# -*- coding: utf-8 -*-

import os

from openfisca_core import reforms
from openfisca_core.columns import EnumCol, FloatCol, IntCol, StrCol
from openfisca_core.enumerations import Enum
from openfisca_france.entities import Individus
import numpy as np
import yaml

from . import conv


source_file_dir_name = os.path.dirname(os.path.abspath(__file__))
tabacs_yaml_file_path = os.path.join(source_file_dir_name, 'assets', 'tabacs.yaml')


def match_conditions(yaml_blocks, simulation, period):
    for yaml_block in yaml_blocks:
        simulation_value_by_variable_name = {
            variable_name: np.array(  # FIXME Performance issue here but needed for dealing with Enum labels.
                simulation.get_holder(variable_name).to_value_json(use_label = True)[str(period)]
                )
            for variable_name in yaml_block['conditions']
            }
        condition_tuples = [
            (operator, simulation_value_by_variable_name[variable_name], condition_value)
            for variable_name, (operator, condition_value) in yaml_block['conditions'].iteritems()
            ]
        conditions = [
            operator(simulation_value, condition_value)
            for operator, simulation_value, condition_value in condition_tuples
            ]
        # print simulation_value_by_variable_name
        # print yaml_block['conditions']
        # print conditions
        assert NotImplemented not in conditions, (conditions, condition_tuples)
        if all(conditions):
            # print '===== match', yaml_block
            return yaml_block
    # print '---- no match'
    return None


# Build reform function


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = u'douanes',
        name = u'Droits de douane, droits de consommation et TVA',
        reference = tax_benefit_system,
        )

    with open(tabacs_yaml_file_path, 'r') as tabacs_yaml_file:
        tabacs_yaml_blocks = yaml.load(tabacs_yaml_file)
    tabacs_yaml_blocks = conv.check(conv.validate_yaml_blocks)(tabacs_yaml_blocks)
    yaml_blocks = tabacs_yaml_blocks

    def yaml_tree_variable_function(self, simulation, period):
        match = match_conditions(yaml_blocks, simulation, period)
        result = self.zeros() + match['results'][self.__class__.__name__] \
            if match is not None \
            else self.zeros()
        return period, result

    # Input variables

    class zone_provenance_produit(Reform.Variable):
        column = EnumCol(enum = Enum([u'Andorra', u'non_EU', u'EU']))
        entity_class = Individus
        label = u'Zone de provenance du produit importé'

    class code_produit(Reform.Variable):
        column = StrCol
        entity_class = Individus
        label = u'Code du produit importé suivant la nomenclature des douanes'

    class quantite_produit(Reform.Variable):
        column = IntCol
        entity_class = Individus
        label = u'Quantité du produit importé'

    # Variables with formulas

    class taux_droits_douane_max(Reform.Variable):
        column = FloatCol
        entity_class = Individus
        function = yaml_tree_variable_function
        label = u'Taux de droits de douane sur un produit importé'

    class droits_consommation(Reform.Variable):
        column = FloatCol
        entity_class = Individus
        function = yaml_tree_variable_function
        label = u'Taux de droits de consommation sur un produit importé'

    class tva(Reform.Variable):
        column = FloatCol
        entity_class = Individus
        function = yaml_tree_variable_function
        label = u'Taux de TVA sur un produit importé'

    reform = Reform()
    return reform
