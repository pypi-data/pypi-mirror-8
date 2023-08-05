==========
quicktions
==========

Python's Fraction data type is an excellent way to do exact money
calculations and largely beats Decimal in terms of simplicity,
accuracy and safety.  Clearly not in terms of speed, though, given
the cdecimal accelerator in Py3.3+.

This is an adaptation of the original fractions module (as included
in CPython 3.4) that is compiled and optimised with Cython into a
fast, native extension module.

Compared to the standard library 'fractions' module in Py2.7 and
Py3.4, 'quicktions' is currently about 10x faster, and still about
5x faster than the current version in Python 3.5.  It's also about
15x faster than the (Python implemented) decimal module in Py2.7.

For documentation, see the Python standard library's fraction module:

https://docs.python.org/3.4/library/fractions.html
