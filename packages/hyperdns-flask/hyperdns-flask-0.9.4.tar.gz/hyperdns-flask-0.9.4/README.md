## Connect Flask, SQLAlchemy, and HAL/REST, secured with JWT

Connect Flask, Declarative SQLAlchemy, and HAL using python annotations.  With one set
of annotations and a few custom helpers, you can map your SQLAlchemy model onto a
HAL flavored REST API, with access control governed by JWT.

Documentation: http://hyperdns.github.io/hyperdns-flask-python3

PyPI: http://pypi.python.org/pypi/hyperdns-flask

Other Resources:

* http://stateless.co/hal_specification.html
* https://github.com/mikekelly/hal_specification
* https://tools.ietf.org/html/draft-kelly-json-hal-06


### QuickStart

To get started, you'll need python3 and virtualenv, then just
type the following:

```
    >>> virtualenv -p python3 .python
    >>> . .python/bin/activate
    >>> pip install -e . -r dev-requirements.txt
    >>> nosetests
```



