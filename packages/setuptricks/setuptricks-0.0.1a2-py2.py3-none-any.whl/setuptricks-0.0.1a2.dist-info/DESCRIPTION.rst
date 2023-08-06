setuptricks
-----------

Convenience functions for your setup.py.

|Current PyPi Version| |MIT licensed| |Travis CI Status| |Coverage
Status| |PyPi Monthly Downloads|

Installation
------------

>From pip:

.. code:: sh

    $ pip install setuptricks

Usage
-----

Before calling setuptools' setup:

.. code:: py

    from setuptools import setup
    import setuptricks

    s = setuptricks.Package("name_of_package")

    s.before_setup()
    setup(name=s.package,
          version=s.version,
          description=s.description,
          ...
    )

*See for example this packages setup.py.*

The ``before_setup()`` allows you to run:

.. code:: sh

    $ python setup.py publish
    $ python setup.py tag

As discussed in `pydanny's
blog <http://www.pydanny.com/python-dot-py-tricks.html>`__ and as used
in
`django-rest-framework <https://github.com/tomchristie/django-rest-framework/blob/971578ca345c3d3bae7fd93b87c41d43483b6f05/setup.py#L61-L67>`__.

.. |Current PyPi Version| image:: http://img.shields.io/pypi/v/setuptricks.svg
   :target: https://pypi.python.org/pypi/setuptricks
.. |MIT licensed| image:: http://img.shields.io/badge/license-MIT-brightgreen.svg
   :target: http://choosealicense.com/licenses/mit/
.. |Travis CI Status| image:: http://img.shields.io/travis/hayd/setuptricks.svg
   :target: https://travis-ci.org/hayd/setuptricks/builds
.. |Coverage Status| image:: http://img.shields.io/coveralls/hayd/setuptricks.svg
   :target: https://coveralls.io/r/hayd/setuptricks
.. |PyPi Monthly Downloads| image:: http://img.shields.io/pypi/dm/setuptricks.svg
   :target: https://pypi.python.org/pypi/setuptricks


