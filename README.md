# OpenFisca douanes

Simulateur ouvert de taxes de douanes - en développement

![Project architecture](https://cdn.rawgit.com/openfisca/openfisca-douanes/master/notes/architecture.svg)

> To rebuild the diagram, run in your shell:
```
make notes/architecture.svg
```

## Run tests locally

To run tests on your development machine:

```
make test

# or more verbose:
python openfisca_douanes/tests/test_yaml.py -v

# to enter ipdb debugger when an exception is raised:
nosetests openfisca_douanes/tests/test_yaml.py --ipdb
```

## Test with the Web API locally

You can host locally an instance of the [Web API](https://github.com/openfisca/openfisca-web-api) and configure it
to load the OpenFisca-Douanes extension (this repo).
See [documentation](http://doc.openfisca.fr/openfisca-web-api/index.html).

Example with [`curl`](http://curl.haxx.se/) and [`jq`](https://stedolan.github.io/jq/) from the command line:

```
curl http://localhost:2000/api/1/calculate -X POST --data @./api_tests/douanes_test_1.json  --header 'content-type: application/json' | jq .
```

## Test with the public Web API

OpenFisca web API is configured to load the OpenFisca-Douanes extension (this repo).

Example with [`curl`](http://curl.haxx.se/) and [`jq`](https://stedolan.github.io/jq/) from the command line:

```
curl http://api.openfisca.fr/api/1/calculate -X POST --data @./api_tests/douanes_test_1.json  --header 'content-type: application/json' | jq .
```

Should output a JSON like:

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
          "douanes_zone_provenance_produit": 0,
          "douanes_code_produit": "2402100000",
          "douanes_quantite_produit": 200
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
