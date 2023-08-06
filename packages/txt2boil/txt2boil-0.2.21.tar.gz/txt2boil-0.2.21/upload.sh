#!/bin/bash

python setup.py register
python setup.py sdist bdist_egg upload "$@"
python setup.py bdist_wininst bdist_msi upload "$@"
python setup.py bdist_rpm upload "$@"
