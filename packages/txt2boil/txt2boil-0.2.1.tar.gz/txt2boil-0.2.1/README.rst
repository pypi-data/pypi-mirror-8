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

With this, one can keep the boilerplate in VCS and use txt2boil to
update it whenever they need to.

Installation
------------

The preferred way to install this is using pip::

    pip install txt2boil

Although if you're not a regular pip user or are not used to using pip
then the alternative is to just download the repository with git and
run the setup.py script::

    git clone https://github.com/kcolford/txt2boil.git
    cd txt2boil
    python setup.py install

How To Use
----------

In order to use ``txt2boil`` as in the example above, simply use::

    $ txt2boil -i rational.rkt

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

License
-------

txt2boil is released under the MIT license which can be found in the
file LICENSE.txt.
