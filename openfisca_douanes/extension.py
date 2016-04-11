# -*- coding: utf-8 -*-

import glob
import itertools
import os

from openfisca_core import reforms
from openfisca_core.columns import BoolCol, EnumCol, FloatCol, IntCol, StrCol
from openfisca_core.enumerations import Enum
from openfisca_france.entities import Individus
import numpy as np
import yaml

from . import conv


source_file_dir_name = os.path.dirname(os.path.abspath(__file__))
assets_dir_path = os.path.join(source_file_dir_name, 'assets')
trees_dir_path = os.path.join(assets_dir_path, 'trees')


def match_conditions(yaml_blocks, simulation, period):
    for yaml_block in yaml_blocks:
        simulation_value_by_variable_name = {
            variable_name: np.array(  # FIXME Performance issue here but needed for dealing with Enum labels.
                simulation.get_holder(variable_name).to_value_json(use_label = True)[str(period)]
                )
            for variable_name in yaml_block['conditions']
            }
        match = all(
            condition_expression.evaluate({'value': value})
            for variable_name, condition_expression in yaml_block['conditions'].iteritems()
            for value in simulation_value_by_variable_name[variable_name]
            )
        if match:
            return yaml_block
    return None


def read_yaml_categories_produits():
    yaml_file_path = os.path.join(assets_dir_path, 'categories-produits.yaml')
    with open(yaml_file_path, 'r') as yaml_file:
        categories_produits = yaml.load(yaml_file)
    categories_produits, errors = conv.validate_yaml_categories_produits(categories_produits)
    assert errors is None, 'Error in "{}": {}'.format(yaml_file_path, errors)
    return categories_produits


def read_yaml_tree(yaml_file_path, validate_yaml_tree):
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_blocks = yaml.load(yaml_file)
    yaml_blocks, errors = validate_yaml_tree(yaml_blocks)
    assert errors is None, 'Error in "{}": {}'.format(yaml_file_path, errors)
    return yaml_blocks


# Build reform function


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = u'douanes',
        name = u'Droits de douane, droits de consommation et TVA',
        reference = tax_benefit_system,
        )

    def yaml_tree_variable_function(self, simulation, period):
        # yaml_blocks is defined in outer scope
        match = match_conditions(yaml_blocks, simulation, period)
        result = self.zeros() + match['results'][self.__class__.__name__] \
            if match is not None \
            else self.zeros()
        return period, result

    # Input variables

    class code_produit(Reform.Variable):
        column = StrCol
        entity_class = Individus
        label = u'Code du produit importé suivant la nomenclature des douanes'

    class moyen_transport(Reform.Variable):
        column = EnumCol(enum = Enum([u'avion', u'bateau', u'route', u'train']))
        entity_class = Individus
        label = u'Moyen de transport utilisé pour importer un produit'

    class quantite_produit(Reform.Variable):
        column = IntCol
        entity_class = Individus
        label = u'Quantité du produit importé'

    class valeur_produit(Reform.Variable):
        column = FloatCol
        entity_class = Individus
        label = u'Valeur du produit importé'

    class zone_provenance_produit(Reform.Variable):
        column = EnumCol(enum = Enum([u'Andorra', u'non_EU', u'EU']))
        entity_class = Individus
        label = u'Zone de provenance du produit importé'

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

    class droits_specifiques(Reform.Variable):
        column = FloatCol
        entity_class = Individus
        function = yaml_tree_variable_function
        label = u'TODO'

    class tva(Reform.Variable):
        column = FloatCol
        entity_class = Individus
        function = yaml_tree_variable_function
        label = u'Taux de TVA sur un produit importé'

    class importation_interdite(Reform.Variable):
        column = BoolCol
        entity_class = Individus
        function = yaml_tree_variable_function
        label = u'L\'importation du produit est interdite'

    # This creates reform.column_by_name
    reform = Reform()

    categories_produits = read_yaml_categories_produits()
    validate_yaml_tree = conv.make_validate_yaml_tree(
        categories_produits = categories_produits,
        variable_names = reform.column_by_name.keys(),
        )
    yaml_file_paths = glob.glob(os.path.join(trees_dir_path, '*.yaml'))
    yaml_blocks = list(itertools.chain.from_iterable(
        read_yaml_tree(yaml_file_path, validate_yaml_tree)
        for yaml_file_path in yaml_file_paths
        ))

    return reform
