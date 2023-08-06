argspander
====
Python package that provides argument expansion of objects.

Why:
----
It was created to enable a sane way of entering arguments gathered from
argparse into your program, without the need to pass round an arguments object.

Usage:
----
>>> import argspander
>>> @argspander.expand
... def f(a, b, c):
...     print "a: %s, b: %s, c: %s" % (a, b, c)
>>> f(3, 2, 1)
a: 3, b: 2, c: 1
>>> class Args():  # similar to the object return by argparse
...     a = 3
...     b = 2
...     c = 1
>>>  f(Args(), expand=True)
a: 3, b: 2, c: 1
