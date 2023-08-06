txt2boil
========

This is a boilerplate generator that generates code based on the
comments it finds in source code.  

Motivation
----------

The motivation is that ordinary boilerplate generators either require
you to hack the build system you're using (to build the source code on
the fly) or you statically generate the boiler plate (and are then
unable to modify it or generate more without pulling together the
script that first generated it).

The original use of this was to generate definitions of constants in
homework assignments done in the Racket programming language.  So as
an example of writing a test code for rational number data-type::

    ;; Constant Gen: r([0-9]+)/([0-9]+) (make-rational \1 \2)
    
    (check-expect (rational-add r7/9 r5/6) r29/18)

Would become::

    ;; Constant Gen: r([0-9]+)/([0-9]+) (make-rational \1 \2)
    (define r29/18 (make-rational 29 18))
    (define r5/6 (make-rational 5 6))
    (define r7/9 (make-rational 7 9))

    (check-expect (rational-add r7/9 r5/6) r29/18)

And no matter how many times you run the program on the source file,
it will only generate the same output, or add/remove boilerplate
according to how the source file changed.

With this, one can keep the boilerplate in VCS and use ``txt2boil`` to
update it whenever they need to.

Installation
------------

The preferred way to install this is using pip::

    pip install txt2boil

Although if you're not a regular pip user or are not used to using pip
then the alternative is to just download the repository with git::

    git clone https://github.com/kcolford/txt2boil.git
    cd txt2boil

Or you can download the tar package from the PyPi website by `clicking
here <https://pypi.python.org/pypi/txt2boil>`_ and then clicking on
the big green Download icon.  Alternatively you can use ``wget`` (or
``curl`` if you prefer)::

    wget https://pypi.python.org/packages/source/t/txt2boil/txt2boil-x.x.x.tar.gz

Once you have the tar ball, unpack it and change to the directory
containing it::

    tar xf txt2boil-x.x.x.tar.gz
    cd txt2boil-x.x.x

Once you're in the source repository (regardless of how you got it)
run the ``setup.py`` script::

    python setup.py install

How To Use
----------

In order to use ``txt2boil`` as in the example above, simply use::

    txt2boil -i rational.rkt

The ``-i`` option specifies to update the file in place rather than
outputting it on stdout.

Supported Languages
-------------------

Language support all depends on what language the package's core
library has functionality for.  The current languages that are
supported are:

- C
- C++
- Java
- Python
- Racket

Internet Presence 
-----------------

There are two significant web resources for txt2boil.  The first is
the source repository and the second is the PyPi page.  Regardless of
which one you go to, this document ought to be the main page found
there.

The primary source repository can be found at `Git Hub
<https://github.com/kcolford/txt2boil>`_ while the PyPi (Python
Package Index) page can be found `here
<https://pypi.python.org/pypi/txt2boil/>`_.

While the Git Hub repository only has source code, the PyPi page has
downloads for binary distributions.  These binary distributions are
provided by anyone generous enough to lend their computer to the task
of compiling them and uploading them.  Anyone who has privileges to
upload to PyPi need only run either the shell script ``upload.sh``
**or** the batch script ``upload.bat``.

License
-------

Copyright (C) 2014 Kieran Colford

This file is part of txt2boil.

txt2boil is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.
 
txt2boil is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with txt2boil.  If not, see <http://www.gnu.org/licenses/>.

