"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
Autogenerated by poetry-setup:
https://github.com/orsinium/poetry-setup
"""
# IMPORTANT: this file is autogenerated. Do not edit it manually.
# All changes will be lost after `poetry-setup` command execution.
# ----------------------------------------------------------------
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open
here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
setup(
    # https://packaging.python.org/specifications/core-metadata/#name
    name='negmas',  # Required
    # https://www.python.org/dev/peps/pep-0440/
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.43',  # Required
    # https://packaging.python.org/specifications/core-metadata/#summary
    description="NEGotiations Managed by Agent Simulations",  # Required
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,  # Optional
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url="https://github.com/yasserfarouk/negmas",  # Optional
    author="Yasser Mohammad",  # Optional
    author_email="yasserfarouk@gmail.com",  # Optional
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],  # Optional
    keywords=' '.join(['negotiation', 'mas', 'multi-agent', 'simulation',
                       'AI']),  # Optional
    packages=find_packages(exclude=[
        'negmas/**/*.pyc',
        'nemgas/**/__pycache__',
        'config',
        'docs',
        'etc',
        'notebooks',
        'tests',
    ]),  # Required
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'Click (>=6.0)',
        'dataclasses; python_version < "3.7"',
        'PyYAML (==5.1b1)',
        'progressbar2 (>=3.39,<4.0)',
        'typing_extensions (>=3.7,<4.0)',
        'pytest-runner (>=4.4,<5.0)',
        'pandas (>=0.24.1,<0.25.0)',
        'scipy (>=1.2,<2.0)',
        'numpy (>=1.16,<2.0)',
        'stringcase (>=1.2,<2.0)',
        'py4j (>=0.10.8,<0.11.0)',
        'colorlog (>=4.0,<5.0)',
        'inflect (>=2.1,<3.0)',
        'matplotlib (>=3.0,<4.0)',
        'setuptools (>=40.8,<41.0)',
        'tabulate (>=0.8.3,<0.9.0)',
        'typing (>=3.6,<4.0)',
        'tox (>=3.7,<4.0)',
    ],  # Optional
    # https://setuptools.readthedocs.io/en/latest/setuptools.html#dependencies-that-aren-t-in-pypi
    dependency_links=[],  # Optional
    # https://stackoverflow.com/a/16576850
    include_package_data=True,
    entry_points={  # Optional
        'console_scripts': [
            'negmas=negmas.scripts.app:cli',
        ],
    },
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    project_urls={  # Optional
        'homepage': 'https://github.com/yasserfarouk/negmas',
    },
)
