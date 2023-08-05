Flask-GCM
=========

| |Build Status|
| |Coverage Status|
| |PyPI Version|
| |PyPI Downloads|

Flask-GCM is a simple wrapper for the
```gcm-client`` <https://pypi.python.org/pypi/gcm-client/>`__ library to
be used with `Flask <http://flask.pocoo.org/>`__ applications.

Getting Started
---------------

Requirements
~~~~~~~~~~~~

-  Python 2.6+ or Python 3.3+

Installation
~~~~~~~~~~~~

Flask-GCM can be installed with pip:

::

    $ pip install flask-gcm

or directly from the source code:

::

    $ git clone https://github.com/MichiganLabs/flask-gcm.git
    $ cd flask-gcm
    $ python setup.py install

Basic Usage
~~~~~~~~~~~

.. code:: python

    from flask import Flask
    from flask.ext.gcm import GCM

    app = Flask(__name__)
    gcm = GCM(app)

Flask-GCM also supports the Flask `"app
factory" <http://flask.pocoo.org/docs/0.10/patterns/appfactories/>`__
paradigm using ``init_app``:

.. code:: python

    from flask import Flask
    from flask.ext.gcm import GCM

    gcm = GCM()

    def create_app():
        app = Flask(__name__)
        gcm.init_app(app)
        return app

The ``gcm`` object can then be used as described in the ```gcm-client``
docs <http://gcm-client.readthedocs.org/en/latest/index.html>`__

For Contributors
----------------

Requirements
~~~~~~~~~~~~

-  GNU Make:

   -  Windows: http://cygwin.com/install.html
   -  Mac: https://developer.apple.com/xcode
   -  Linux: http://www.gnu.org/software/make (likely already installed)

-  virtualenv: https://pypi.python.org/pypi/virtualenv#installation

Installation
~~~~~~~~~~~~

Create a virtualenv:

::

    $ make env

Run the tests:

::

    $ make test

Build the documentation:

::

    $ make doc

Run static analysis:

::

    $ make flake8
    $ make pep257
    $ make check  # includes all checks

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

Contributions are always welcome! Please keep the following in mind when
creating a pull request:

-  Include (passing) tests for all new features and bugfixes
-  Contributed code should pass ``flake8`` checks
-  Include documentation which passes ``pep257`` guidelines

.. |Build Status| image:: http://img.shields.io/travis/MichiganLabs/flask-gcm/master.svg
   :target: https://travis-ci.org/MichiganLabs/flask-gcm
.. |Coverage Status| image:: http://img.shields.io/coveralls/MichiganLabs/flask-gcm/master.svg
   :target: https://coveralls.io/r/MichiganLabs/flask-gcm
.. |PyPI Version| image:: http://img.shields.io/pypi/v/flask-gcm.svg
   :target: https://pypi.python.org/pypi/flask-gcm
.. |PyPI Downloads| image:: http://img.shields.io/pypi/dm/flask-gcm.svg
   :target: https://pypi.python.org/pypi/flask-gcm

Changelog
=========

0.0.1 (2014/10/13)
------------------

 - Initial release


