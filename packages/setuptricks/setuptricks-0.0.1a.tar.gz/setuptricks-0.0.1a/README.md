setuptricks
-----------

Convenience functions for your setup.py.

[![Current PyPi Version](http://img.shields.io/pypi/v/setuptricks.svg)](https://pypi.python.org/pypi/setuptricks)
[![MIT licensed](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://choosealicense.com/licenses/mit/)
[![Travis CI Status](http://img.shields.io/travis/hayd/setuptricks.svg)](https://travis-ci.org/hayd/setuptricks/builds)
[![Coverage Status](http://img.shields.io/coveralls/hayd/pep8radius.svg)](https://coveralls.io/r/hayd/setuptricks)
[![PyPi Monthly Downloads](http://img.shields.io/pypi/dm/pep8radius.svg)](https://pypi.python.org/pypi/setuptricks)


Installation
------------
From pip:

```sh
$ pip install setuptricks
```

Usage
-----
Before calling setupetools' setup:
```py
import setuptricks

setuptricks.before_setup()
```

