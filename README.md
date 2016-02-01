# OpenFisca douanes

[![Build Status](https://travis-ci.org/openfisca/openfisca-douanes.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-douanes)

Simulateur ouvert de taxes de douanes - en développement

![Project architecture](https://rawgit.com/openfisca/openfisca-douanes/master/notes/architecture.svg)

> Memento pour reconstruire le diagramme :
```
make notes/architecture.svg
```

## Client de démo

Un client de démonstration volontairement minimal est disponible ici : http://output.jsbin.com/lusime

> Son code source est [ici](http://jsbin.com/lusime/edit)

## Tester avec l'API Web publique d'OpenFisca

Example avec [`curl`](http://curl.haxx.se/) et [`jq`](https://stedolan.github.io/jq/):

```
curl http://api.openfisca.fr/api/1/calculate -X POST --data @./api_tests/douanes_test_1.json  --header 'content-type: application/json' | jq .
```

Devrait répondre un JSON de ce type :

```json
{
  "apiVersion": 1,
  "method": "/api/1/calculate",
  "params": {
    "base_reforms": [
      "douanes"
    ],
    "scenarios": [
      {
        "period": "2015",
        "input_variables": {
          "zone_provenance_produit": 0,
          "code_produit": "2402100000",
          "quantite_produit": 200
        }
      }
    ],
    "output_format": "variables",
    "variables": [
      "droits_consommation",
      "taux_droits_douane_max",
      "tva"
    ]
  },
  "url": "http://api.openfisca.fr/api/1/calculate",
  "value": [
    {
      "taux_droits_douane_max": {
        "2015": [
          0.25999999046325684
        ]
      },
      "droits_consommation": {
        "2015": [
          -1
        ]
      },
      "tva": {
        "2015": [
          0.20000000298023224
        ]
      }
    }
  ]
}
```

## Exécuter les tests localement

Sur la machine de développement :

```
make test

# or more verbose:
python openfisca_douanes/tests/test_yaml.py -v

# to enter ipdb debugger when an exception is raised:
nosetests openfisca_douanes/tests/test_yaml.py --ipdb
```

## Tester avec une instance locale de l'API Web

Vous pouvez faire tourner une instance de l'[API Web](https://github.com/openfisca/openfisca-web-api) et la configurer pour charger l'extension OpenFisca-Douanes (ce repo).
Voir la [documentation](http://doc.openfisca.fr/openfisca-web-api/index.html).

Example avec [`curl`](http://curl.haxx.se/) et [`jq`](https://stedolan.github.io/jq/) :

```
curl http://localhost:2000/api/1/calculate -X POST --data @./api_tests/douanes_test_1.json  --header 'content-type: application/json' | jq .
```

Devrait répondre un JSON du même type que ci-dessus.
