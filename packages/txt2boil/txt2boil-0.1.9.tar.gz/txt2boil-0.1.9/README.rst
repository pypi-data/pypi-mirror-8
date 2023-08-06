txt2boil
********

This is a boilerplate generator that generates code based on the
comments it finds in source code.

Installation
============

The preferred way to install this is using pip::

    pip install txt2boil

Although if you're not a regular pip user or are not used to using pip
then the alternative is to just download the repository with git and
run the setup.py script::

    git clone https://github.com/kcolford/txt2boil.git
    cd txt2boil
    python setup.py install

Motivation
==========

The motivation is that ordinary boilerplate generators either require
you to hack the build system you're using (to build the source code on
the fly) or you statically generate the boiler plate (and are then
unable to modify it or generate more without pulling together the
script that first generated it).

