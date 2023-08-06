Syncify
=======

This package is meant for wrapping asynchronous functions so that they
behave like synchronous functions. This package is very useful when
scripting.

Getting Started
---------------

::

    pip install syncify

Usage
-----

Suppose you have an asynchronous function called ``asyncFunction`` that
has a keyword arguement, ``'callback'`` for the callback function. You
can run it synchronously like this:

::

    from syncify import syncify

    results syncify(asyncFunction, kw='callback')(arguments)

They keyword, ``kw`` is set to ``'callback'`` by default so that can be
left off, but I left it there in case someone has a different callback
keyword.
