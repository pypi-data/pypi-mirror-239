yatp
====

Yet Another Test Project.

Example
_______

.. code-block:: python

    from yatp import timer

    @timer
    def some_function():
        return [x for x in range(10_000_000)]