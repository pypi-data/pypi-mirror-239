#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('./src/genomoncology/README.md') as readme_file:
    readme = readme_file.read()

history = ""

tests_require = [
    "flake8 == 6.1.0",
    "black == 23.10.1",
    "ipython == 8.17.2",
    "pytest == 7.4.3",
    "pytest-cov == 4.1.0",
    "white == 0.1.2",
    "pytest-socket == 0.6.0",
    "pytest-asyncio == 0.21.1",
    "aioconsole == 0.6.2",
    "addict == 2.4.0",
    "requests >= 2.31.0",
    "twine == 4.0.2",
    "readme-renderer == 42.0"
]

setup(
    name="gocli",
    version='0.10.1',
    author="Ian Maurer",
    author_email='ian@genomoncology.com',

    packages=[
        "genomoncology",
        "genomoncology.kms",
        "genomoncology.cli",
        "genomoncology.parse",
        "genomoncology.pipeline",
        "genomoncology.pipeline.sinks",
        "genomoncology.pipeline.sources",
        "genomoncology.pipeline.sources.one_off_sources",
        "genomoncology.pipeline.transformers",
        "genomoncology.pipeline.transformers.tx",
        "gosdk",
        "govcf",
        "govcf.calculate_vaf",

    ],
    package_dir={
        '': 'src'
    },

    package_data={
        '': ["*.yaml", "*.bed", "*.txt", "*.tsv", "*.csv"]
    },

    include_package_data=True,

    tests_require=tests_require,
    install_requires=[
        "related >= 0.7.3",
        "backoff == 2.2.1",
        "click == 8.1.7",
        "structlog == 23.2.0",
        "colorama == 0.4.6",
        "pysam == 0.22.0",
        "ujson == 5.8.0",
        "intervaltree == 3.1.0",
        "glom == 23.3.0",
        "cytoolz == 0.12.2",
        "openpyxl == 3.1.2",
        "pygments == 2.16.1",
        "jsonschema[format] == 4.19.2",
        "flask == 1.0.2",
        "itsdangerous == 2.1.1",
        "Werkzeug == 3.0.1",
        "jinja2 == 3.1.2",
        "flask-swagger-ui == 4.11.1",
        "swagger-spec-validator == 3.0.3",
        "PyYAML == 6.0.1",
        "dictdiffer == 0.9.0",
        "inflect == 7.0.0",
        "aiobravado == 0.9.2",
        "bravado == 11.0.3",
        "bravado-core == 6.1.0",
        "bravado-asyncio == 2.0.2",
        "stringcase == 1.2.0",
        "urllib3 == 2.0.7",
    ],

    setup_requires=[
        'pytest-runner',
    ],

    license="Proprietary",
    keywords='Bioinformatics HGVS VCF Clinical Trials Genomics',

    description="gocli",
    long_description="%s\n\n%s" % (readme, history),

    entry_points={
        'console_scripts': [
            'gocli=genomoncology.main:main',
        ],
    },

    classifiers=[
        'License :: Other/Proprietary License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)
