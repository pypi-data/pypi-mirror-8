hiyapyco
========

HiYaPyCo - A Hierarchical Yaml Python Config

Description
-----------

A simple python lib allowing hierarchical overlay of config files in
YAML syntax, offering different merge methods and variable interpolation
based on jinja2.

Key Features
------------

-  hierarchical overlay of multiple YAML files
-  multiple merge methods for hierarchical YAML files
-  variable interpolation using jinja2

Requirements
------------

-  PyYAML aka. python-yaml
-  Jinja2 aka. python-jinja2
-  ordereddict for python2.6 (if you like to use the Ordered Dict Yaml
   Loader / Dumper aka. ODYLDo)

Python Version
~~~~~~~~~~~~~~

HiYaPyCo was designed to run on both current major python versions
without changes. Tested versions:

-  2.6
-  2.7
-  3.2

Usage
-----

A simple example:

::

    import hiyapyco
    conf = hiyapyco.load('yamlfile1' [,'yamlfile2' [,'yamlfile3' [...]]] [,kwargs])
    print(hiyapyco.dump(conf))

real life example:
~~~~~~~~~~~~~~~~~~

``yaml1.yaml``:

::

    ---
    first: first element
    second: xxx
    deep:
        k1:
            - 1
            - 2

``yaml2.yaml``:

::

    ---
    second: again {{ first }}
    deep:
        k1:
            - 4 
            - 6
        k2:
            - 3
            - 6

load ...

::

    >>> import pprint
    >>> import hiyapyco
    >>> conf = hiyapyco.load('yaml1.yaml', 'yaml2.yaml', method=hiyapyco.METHOD_MERGE, interpolate=True, failonmissingfiles=True)
    >>> pprint.PrettyPrinter(indent=4).pprint(conf)
    {   'deep': {   'k1': [1, 2, 4, 6], 'k2': [3, 6]},
        'first': u'first element',
        'ma': {   'ones': u'12', 'sum': u'22'},
        'second': u'again first element'}

args
~~~~

All ``args`` are handled as file names. They may be strings or list of
strings.

kwargs
~~~~~~

-  ``method``: bit (one of the listed below):

   -  ``hiyapyco.METHOD_SIMPLE``: replace values (except for lists a
      simple merge is performed) (default method)
   -  ``hiyapyco.METHOD_MERGE``: perform a deep merge

-  ``interpolate``: boolean : perform interpolation after the merge
   (default: False)

-  ``usedefaultyamlloader``: boolean : force the usage of the default
   *PyYAML* loader/dumper instead of *HiYaPyCo*\ s implementation of a
   OrderedDict loader/dumper (see: Ordered Dict Yaml Loader / Dumper
   aka. ODYLDo) (default: False)

-  ``failonmissingfiles``: boolean : fail if a supplied YAML file can
   not be found (default: True)

-  ``loglevel``: int : loglevel for the hiyapyco logger; should be one
   of the valid levels from ``logging``: 'WARN', 'ERROR', 'DEBUG', 'I
   NFO', 'WARNING', 'CRITICAL', 'NOTSET' (default: default of
   ``logging``)

-  ``loglevelmissingfiles``: int : one of the valid levels from
   ``logging``: 'WARN', 'ERROR', 'DEBUG', 'INFO', 'WARNING', 'CRITICAL',
   'NOTSET' (default: ``logging.ERROR`` if
   ``failonmissingfiles = True``, else ``logging.WARN``)

interpolation
~~~~~~~~~~~~~

For using interpolation, I strongly recomend *not* to use the default
PyYAML loader, as it sorts the dict entrys alphabetically, a fact that
may break interpolation in some cases (see ``test/odict.yaml`` and
``test/test_odict.py`` for an example). See Ordered Dict Yaml Loader /
Dumper aka. ODYLDo

default
^^^^^^^

The default jinja2.Environment for the interpolation is

::

    hiyapyco.jinja2env = Environment(undefined=Undefined)

This means that undefined vars will be ignored and replaced with a empty
string.

change the jinja2 Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you like to change the jinja2 Environment used for the interpolation,
set ``hiyapyco.jinja2env`` **before** calling ``hiyapyco.load``!

use jinja2 DebugUndefined
^^^^^^^^^^^^^^^^^^^^^^^^^

If you like to keep the undefined var as string but raise no error, use

::

    from jinja2 import Environment, Undefined, DebugUndefined, StrictUndefined
    hiyapyco.jinja2env = Environment(undefined=DebugUndefined)

use jinja2 StrictUndefined
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you like to raise a error on undefined vars, use

::

    from jinja2 import Environment, Undefined, DebugUndefined, StrictUndefined
    hiyapyco.jinja2env = Environment(undefined=StrictUndefined)

This will raise a ``hiyapyco.HiYaPyCoImplementationException`` wrapped
arround the ``jinja2.UndefinedError`` pointing at the strig causing the
error.

more informations
^^^^^^^^^^^^^^^^^

See:
`jinja2.Environment <http://jinja.pocoo.org/docs/dev/api/#jinja2.Environment>`_

Ordered Dict Yaml Loader / Dumper aka. ODYLDo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a simple implementation of a PyYAML loader / dumper using
``OrderedDict`` from collections.
**Because chaos is fun but order matters on loading dicts from a yaml
file.**
In order to use this on python 2.6, please install ordereddict:

::

    sudo pip-2.6 install ordereddict

Install
-------

>From Source
~~~~~~~~~~~

GitHub
^^^^^^

::

    git clone https://github.com/zerwes/hiyapyco
    cd hiyapyco
    sudo python setup.py install

PyPi
^^^^

Download the latest or desired version of the source package from
`https://pypi.python.org/pypi/HiYaPyCo <https://pypi.python.org/pypi/HiYaPyCo>`_.
Unpack the archive and install by executing:

::

    sudo python setup.py install

pip
~~~

Install the latest wheel package using:

::

    pip install HiYaPyCo

debian packages
~~~~~~~~~~~~~~~

::

    echo "deb http://repo.zero-sys.net/hiyapyco/deb ./" > /etc/apt/sources.list.d/hiyapyco.list
    gpg --keyserver keys.gnupg.net --recv-key ED7D414C
    # or use:
    wget http://jwhoisserver.net/key.asc -O - | gpg --import -
    gpg --armor --export ED7D414C | apt-key add -
    apt-get update
    apt-get install python3-hiyapyco python-hiyapyco

rpm packages
~~~~~~~~~~~~

use
`http://repo.zero-sys.net/hiyapyco/rpm <http://repo.zero-sys.net/hiyapyco/rpm>`_
as URL for the yum repo and
`http://jwhoisserver.net/key.asc <http://jwhoisserver.net/key.asc>`_ as
the URL for the key.

License
-------

(c) 2014 Klaus Zerwes `zero-sys.net <http://zero-sys.net>`_
    This package is free software.
    This software is licensed under the terms of the GNU LESSER GENERAL
    PUBLIC LICENSE version 3 or later, as published by the Free Software
    Foundation.
    See
    `https://www.gnu.org/licenses/lgpl.html <https://www.gnu.org/licenses/lgpl.html>`_

Changelog
---------

0.1.0 / 0.1.1
~~~~~~~~~~~~~

Initial release

0.2.0
~~~~~

Fixed unicode handling

0.3.0 / 0.3.1
~~~~~~~~~~~~~

Implemented a Ordered Dict Yaml Loader

0.3.2
~~~~~

Improved tests and bool args checks


