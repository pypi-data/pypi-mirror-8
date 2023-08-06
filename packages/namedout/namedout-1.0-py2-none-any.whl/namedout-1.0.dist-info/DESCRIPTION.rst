*Debug output named values*

warning:
 - not work in python console
 - not work in IDLE
 - only one entry point of dbg function for one source line

script::

    from namedout import dbg
    dbg(dict(a=9))

out::

    dict(a=9) == {'a': 9}

script::

    dbg(list(xrange(9)))

out::

    list(xrange(9)) == [0, 1, 2, 3, 4, 5, 6, 7, 8]

script::

    import os
    import sys
    a = 1
    dbg(a, os.__name__, dir(os.path)[0], sys.modules.keys()[0])

out::

    a == 1
    os.__name__ == os
    dir(os.path)[0] == __all__
    sys.modules.keys()[0] == tokenize



