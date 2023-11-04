# EconomPy - The Econometric Python Library

![Python](https://img.shields.io/badge/python-3.12-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build](https://github.com/malill/econompy/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/malill/econompy/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/malill/econompy/graph/badge.svg?token=AV6JEZMSIP)](https://codecov.io/gh/malill/econompy)
[![Documentation](https://img.shields.io/badge/ref-Documentation-blue)](https://malill.github.io/econompy/)

> The motivation behind the EconomPy library is to provide a set of tools for econometric analysis in Python. Instead of using R (Studio) or Stata for econometric analysis, the goal is to provide a Python alternative.

The EconomPy library is a collection of econometric functions and classes written in Python. The library is designed to be used in conjunction with the [Pandas](https://pandas.pydata.org/) library.

## Installation

For the latest stable version, install from [PyPi](https://pypi.org/project/econompy/):

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the package from PyPi
pip install econompy
```

## Usage

```python
import econompy as ep
```

## Development

To contribute to the development of EconomPy, clone the repository and install the development dependencies.

### Install the Development Dependencies

```bash
# Clone the repository
git clone https://github.com/malill/econompy.git

# Create a virtual environment
python -m venv .venv

# Install the development dependencies
pip install -r requirements-dev.txt

# Install the package in editable mode
pip install -e .
```

### Use pre-commit hooks

The pre-commit hooks are used to ensure that the code is formatted correctly and that the tests pass before committing the code.

```bash
# Install the pre-commit package
pre-commit install

# (To locally) Run the pre-commit hooks
pre-commit run --all-files
```

### Run Code Coverage

You can test the code coverage by running the following command:

```bash
# Run the code coverage
pytest --cov=econompy --cov-report=html
```

This will generate a HTML report in the `htmlcov` folder. Inspect the report by opening the `index.html` file in your browser.
