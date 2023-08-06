Tortilla
========

A tiny Python library for creating wrappers around external APIs.

Usage::

    >>> import tortilla
    >>> github = tortilla.wrap('https://api.github.com')
    >>> redodo = github.users.get('redodo')
    >>> redodo.id
    2227416


