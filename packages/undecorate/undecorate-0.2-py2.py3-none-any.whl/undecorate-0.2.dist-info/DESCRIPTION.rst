undecorate
==========

Let your decorations be undone

Installation
------------

.. code-block:: sh

    $ pip install undecorate

Usage
-----

.. code-block:: pycon

    >>> from undecorate import unwrap, unwrappable
    >>>
    >>> @unwrappable
    ... def pack(func):
    ...     def wrapper(args, kwargs):
    ...        return func(*args, **kwargs)
    ...     return wrapper
    ...
    >>> @pack
    ... def myfunc(a, b=None, c=None):
    ...     return (a, b, c)
    ...
    >>> myfunc('a', b='b')
    Traceback (most recent call last):
        ...
    TypeError: wrapper() got an unexpected keyword argument 'b'
    >>>
    >>> unwrap(myfunc)('a', b='b')
    ('a', 'b', None)


0.2
+++

* Add ``create_class_wrapper`` and ``class_wraps``.
* Internally use ``__wrapped__`` to match Python 3.2+.
* Add backport versions of functools ``wraps`` and ``update_wrapper``.
  They wrap the stdlib versions, and ensure that ``__wrapped__`` is set.


0.1 (2014-09-04)
++++++++++++++++

* Initial Release
* ``unwrappable`` and ``unwrap`` functions


