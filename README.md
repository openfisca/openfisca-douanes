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

## Generate diagram

To build file.svg from file.dot, run in your shell:

```
make path-to/file.svg
```
