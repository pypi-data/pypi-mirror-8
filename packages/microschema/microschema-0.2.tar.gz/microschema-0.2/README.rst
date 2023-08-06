MicroSchema
-----------

MicroSchema is a schema validation framework for Python. It is light, fast and
easy to use.

Example
-------

.. code-block:: python

    >>> import microschema
    >>> schema = {
    ...     'username': {'type': str, 'required': True},
    ...     'score': {'type': int},
    ... }
    >>> data = {
    ...     'username': 'foobar',
    ...     'score': 10000,
    ... }
    >>> print microschema.validate(schema, data)


Features
--------

- Intuitive to use
- Fast (see comparison_ section below)
- Support custom validator
- Nested error messages

.. _comparison:

Installation
------------

To install MicroSchema, simply:

.. code-block:: bash

    $ pip install microschema


Comparison
----------




