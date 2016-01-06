#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Douanes extension for OpenFisca French tax-benefit system"""


from setuptools import setup, find_packages


classifiers = """\
Development Status :: 2 - Pre-Alpha
Environment :: Web Environment
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: POSIX
Programming Language :: Python
Topic :: Scientific/Engineering :: Information Analysis
"""

doc_lines = __doc__.split('\n')


setup(
    name = 'OpenFisca-Douanes',
    version = '0.0.dev0',

    author = 'OpenFisca Team and Douanes Team',
    author_email = 'contact@openfisca.fr',
    classifiers = [classifier for classifier in classifiers.split('\n') if classifier],
    description = doc_lines[0],
    keywords = 'douanes benefit microsimulation server social tax user',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description = '\n'.join(doc_lines[2:]),
    url = 'https://github.com/openfisca/openfisca-douanes',

    install_requires = [
        'numpy >= 1.6,< 1.10',
        'OpenFisca-Core >= 0.5.3.dev0',
        'OpenFisca-France >= 0.5.4.dev0',
        ],
    packages = find_packages(),
    zip_safe = False,
    )
