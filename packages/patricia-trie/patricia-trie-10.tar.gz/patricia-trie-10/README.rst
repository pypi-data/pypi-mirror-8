patricia-trie
=============

A pure Python 2.7+ implementation of a PATRICIA trie for effcient matching
of string collections on text.

Note that you probably first want to have a look at the Python wrapper
`marisa-trie`_ or its `PyPi package <https://github.com/kmike/marisa-trie/>`_
before using particia-trie; according to simple timeit comparisons, these
wrappers for the C-based MARISA library are about twice as fast as this pure
Python implementation.

`patricia-trie`_ does have its merits, however - it is small, clear, and
has a very clean interface that imitates the `dict` API and works with Py3k.

Installation
------------

::

  pip install patricia-trie

Usage
-----

::

    >>> T = trie('root', key='value', king='kong') # a root value and two pairs
    >>> T['four'] = None # setting new values as in a dict
    >>> '' in T # check if the value exits (note: the [empty] root is '')
    True
    >>> 'kong' in T # existence checks as in a dict
    False
    >>> T['king'] # get the value for an exact key ... as in a dict
    'kong'
    >>> T['kong'] # error from non-existing keys (as in a dict)
    Traceback (most recent call last):
        ...
    KeyError: 'kong'
    >>> len(T) # count keys ("terminals") in the tree
    4
    >>> sorted(T) # plus "traditional stuff": .keys(), .values(), and .items()
    ['', 'four', 'key', 'king']
    >>> # scanning a string S with key(S), value(S), and item(S):
    >>> S = 'keys and kewl stuff'
    >>> T.key(S) # report the (longest) key that is a prefix of S
    'key'
    >>> T.value(S, 9) # using offsets; NB: a root value always matches!
    'root'
    >>> del T[''] # interlude: deleting keys (here, the root)
    >>> T.item(S, 9) # raise error if no key is a prefix of S
    Traceback (most recent call last):
        ...
    KeyError: 'k'
    >>> # info: the error string above contains the matched path so far
    >>> T.item(S, 9, default=None) # avoid the error by specifying a default
    (None, None)
    >>> # iterate all matching content with keys(S), values(S), and items(S):
    >>> list(T.items(S))
    [('key', 'value')]
    >>> T.isPrefix('k') # reverse lookup: check if S is a prefix of any key
    True
    >>> T.isPrefix('kong')
    False
    >>> sorted(T.iter('k')) # and get all keys that have S as prefix
    ['key', 'king']

*Deleting* entries is a "half-supported" operation only. The key appears
"removed", but the trie is not actually changed, only the node state is
changed from terminal to non-terminal. I.e., if you frequently delete keys,
the compaction will become fragmented and less efficient. To mitigate this
effect, make a copy of the trie (using a copy constructor idiom)::

    T = trie(**T)

If you are only interested in scanning for the *presence* of keys, but do not
care about mapping a value to each key, using ``None`` as the value of your
keys and scanning with ``key(S, None, start=i)`` at every offset ``i`` in the
string ``S`` is perfectly fine (because the return value will be the key
string iff a full match was made and ``None`` otherwise)::

    >>> T = trie(present=None)
    >>> T.key('is absent here', None, start=3) # start scanning at offset 3
    >>> T.key('is present here', None, start=3) # start scanning at offset 3
    'present'

API
---

trie(``*value``, ``**branch``)
    | Create a new tree node.
    | Any arguments will be used as the ``value`` of this node.
    | If keyword arguments are given, they initialize a whole ``branch``.
    | Note that `None` is a valid value for a node.

trie.isPrefix(``prefix``)
    | Return True if any key starts with ``prefix``.

trie.item(``string``, ``start=0``, ``end=None``, ``default=NULL``)
    | Return the key, value pair of the longest key that is a prefix of ``string`` (beginning at ``start`` and ending at ``end``).
    | If no key matches, raise a `KeyError` or return the `None`, ``default`` pair if any ``default`` value was set.

trie.items([``string`` [, ``start`` [, ``end`` ]]])
    Return all key, value pairs (for keys that are a prefix of ``string``
    (beginning at ``start`` (and terminating before ``end``))).

trie.iter(``prefix``)
    Return an iterator over all keys that start with ``prefix``.

trie.key(``string``, ``start=0``, ``end=None``, ``default=NULL``)
    | Return the longest key that is a prefix of ``string`` (beginning at ``start`` and ending at ``end``).
    | If no key matches, raise a `KeyError` or return the ``default`` value if it was set.

trie.keys([``string`` [, ``start`` [, ``end`` ]]])
    Return all keys (that are a prefix of ``string``
    (beginning at ``start`` (and terminating before ``end``))).

trie.value(``string``, ``start=0``, ``end=None``, ``default=NULL``)
    | Return the value of the longest key that is a prefix of ``string`` (beginning at ``start`` and ending at ``end``).
    | If no key matches, raise a `KeyError` or return the ``default`` value if it was set.

trie.values([``string`` [, ``start`` [, ``end`` ]]])
    Return all values (for keys that are a prefix of ``string``
    (beginning at ``start`` (and terminating before ``end``))).


History
-------

1. Initial release.
2. *Update*: Full documentation and corrections.
3. *Feature*: optional keyword parameters to indicate an offset ``start`` when
   scanning a string with the methods key(), keys(), item(), items(), value(),
   and values(), so it is not necessary to slice strings for each scan::

       >>> # Old usage to scan 'string' in 'the string' was:
       >>> T.keys('the string'[4:])
       >>> # With the new optional keyword parameter:
       >>> T.keys('the string', start=4)

4. **Important API change**: item() now returns key, value pairs even when a
   default value is given, using ``None`` as the "key"::

       >>> # Old behaviour was:
       >>> T.item('string', default=False)
       False
       >>> # While now, the same call produces:
       >>> T.item('string', default=False)
       None, False

   *Improvement*: Switched from using dictionaries to two-tuple lists
   internally (thanks to Pedro Gaio for the suggestion!) to improve the
   overall performance a bit (about 20% faster on simple tests).
5. *Bugfix*: When splitting edges while adding a new key that is shorter than
   the current edge, a index error would have occurred.
6. *Feature*: Added optional keyword parameter ``end`` to the methods key(),
   keys(), item(), items(), value(), and values(), so it is not necessary to
   scan within a window::

       T.key('string', start=2, end=3, default=None)
       T.keys('string', start=2, end=3)

7. *Improvement*: Switched back to a very efficient internal dictionary
   implementation; Runs about two- to three times as fast as the two-tuple
   list from update 4 against the simple (and newly added) ``time_patricia.py``
   "benchmark".
8. *Bugfix*: Correct behavior when using a negative start index.
   Added a comparison to `marisa-trie`_ - by now, it seems, patricia-trie
   is roughly only a factor two slower than the marisa-trie PyPI version
   wrapping a C library. Also makes it nice to compare the two usages.
9. *Bugfix* (15/09/2014): Correct behaviour when using an exactly matching
   prefix as query (issue described in #1 by @zachrahan). Also fixes
   code-smells (PEP8, code complexity) and a failing test case code.
10. *Bugfix* (14/12/2014): Added the missing README to PyPI package.
    (MANIFEST.in)
   
Copyright
---------

Copyright 2013, Florian Leitner. All rights reserved.

License
-------

`Apache License v2 <http://www.apache.org/licenses/LICENSE-2.0.html>`_

.. _marisa-trie: https://code.google.com/p/marisa-trie/
.. _patricia-trie: https://www.github.com/fnl/patricia-trie/
