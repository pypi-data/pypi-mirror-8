#!/bin/bash

./setup.py register sdist bdist_egg upload "$@"
