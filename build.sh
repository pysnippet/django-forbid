#!/bin/bash

# last version of `build` supporting Python 3.6
pip install build==0.9.0

# build the wheel and install it
WHEEL_NAME=$(python -m build | grep -Po "django_forbid-.*\.whl" | tail -n 1)
pip install dist/$WHEEL_NAME