#!/bin/bash

# last version of `build` supporting Python 3.6
pip install build==0.9.0

# build the wheel and install it
python -m build && pip install $(ls dist/django_forbid-*.whl)