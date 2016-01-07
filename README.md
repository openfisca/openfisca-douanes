# OpenFisca douanes

Simulateur ouvert de taxes de douanes - en développement

> Le projet en est à ses premiers stades de développement.

![Project architecture](https://cdn.rawgit.com/openfisca/openfisca-douanes/master/notes/architecture.svg)

## Run tests

```
make test

# or more verbose:
python openfisca_douanes/tests/test_yaml.py -v

# to enter ipdb debugger when an exception is raised:
nosetests openfisca_douanes/tests/test_yaml.py --ipdb
```

## Test the Web API

Example with [`curl`](http://curl.haxx.se/) and [`jq`](https://stedolan.github.io/jq/) from the command line:

```
curl http://localhost:2000/api/1/calculate -X POST --data @./assets/api_tests/douanes_test_1.json  --header 'content-type: application/json' | jq .
```

> Supposing you run an instance of the Web API on your machine: see [documentation](http://doc.openfisca.fr/openfisca-web-api/index.html).

## Generate diagram

To build file.svg from file.dot, run in your shell:

```
make path-to/file.svg
```
