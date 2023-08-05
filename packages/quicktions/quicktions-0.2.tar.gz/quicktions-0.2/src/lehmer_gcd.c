/* Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
 * 2011, 2012, 2013, 2014 Python Software Foundation; All Rights Reserved
 *
 * Copied from CPython 3.4+.
 */

#if CYTHON_USE_PYLONG_INTERNALS && PY_MAJOR_VERSION == 3 && PY_VERSION_HEX <= 0x030500A0
#include "longintrepr.h"

#ifndef Py_ABS
#define Py_ABS(x) ((x) < 0 ? -(x) : (x))
#endif

#ifndef MEDIUM_VALUE
#define MEDIUM_VALUE(x) (assert(-1 <= Py_SIZE(x) && Py_SIZE(x) <= 1),   \
         Py_SIZE(x) < 0 ? -(sdigit)(x)->ob_digit[0] :   \
             (Py_SIZE(x) == 0 ? (sdigit)0 :                             \
              (sdigit)(x)->ob_digit[0]))
#endif

static const unsigned char BitLengthTable[32] = {
    0, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5
};

static int
bits_in_digit(digit d)
{
    int d_bits = 0;
    while (d >= 32) {
        d_bits += 6;
        d >>= 6;
    }
    d_bits += (int)BitLengthTable[d];
    return d_bits;
}

static PyLongObject *
long_normalize(PyLongObject *v)
{
    Py_ssize_t j = Py_ABS(Py_SIZE(v));
    Py_ssize_t i = j;

    while (i > 0 && v->ob_digit[i-1] == 0)
        --i;
    if (i != j)
        Py_SIZE(v) = (Py_SIZE(v) < 0) ? -(i) : i;
    return v;
}

static PyObject *
long_long(PyObject *v)
{
    if (PyLong_CheckExact(v))
        Py_INCREF(v);
    else
        v = _PyLong_Copy((PyLongObject *)v);
    return v;
}

static PyObject *
long_neg(PyLongObject *v)
{
    PyLongObject *z;
    if (Py_ABS(Py_SIZE(v)) <= 1)
        return PyLong_FromLong(-MEDIUM_VALUE(v));
    z = (PyLongObject *)_PyLong_Copy(v);
    if (z != NULL)
        Py_SIZE(z) = -(Py_SIZE(v));
    return (PyObject *)z;
}

static PyObject *
long_abs(PyLongObject *v)
{
    if (Py_SIZE(v) < 0)
        return long_neg(v);
    else
        return long_long((PyObject *)v);
}

static int
long_compare(PyLongObject *a, PyLongObject *b)
{
    Py_ssize_t sign;

    if (Py_SIZE(a) != Py_SIZE(b)) {
        sign = Py_SIZE(a) - Py_SIZE(b);
    }
    else {
        Py_ssize_t i = Py_ABS(Py_SIZE(a));
        while (--i >= 0 && a->ob_digit[i] == b->ob_digit[i])
            ;
        if (i < 0)
            sign = 0;
        else {
            sign = (sdigit)a->ob_digit[i] - (sdigit)b->ob_digit[i];
            if (Py_SIZE(a) < 0)
                sign = -sign;
        }
    }
    return sign < 0 ? -1 : sign > 0 ? 1 : 0;
}

static PyLongObject *
long_gcd(PyLongObject *a, PyLongObject *b)
{
    PyLongObject *c, *d;
    stwodigits x, y, q, s, t, c_carry, d_carry;
    digit A, B, C, D;
    int nbits, k;
    Py_ssize_t size_a, size_b;
    digit *a_digit, *b_digit, *c_digit, *d_digit, *a_end, *b_end;

    /* Initial reduction: make sure that 0 <= b <= a. */
    a = (PyLongObject *)long_abs(a);
    b = (PyLongObject *)long_abs(b);
    if (long_compare(a, b) < 0) {
        d = a;
        a = b;
        b = d;
    }
    /* We now own references to a and b */

    /* reduce until a fits into 2 digits */
    while ((size_a = Py_SIZE(a)) > 2) {
        nbits = bits_in_digit(a->ob_digit[size_a-1]);
        /* extract top 2*PyLong_SHIFT bits of a into x, along with
           corresponding bits of b into y */
        size_b = Py_SIZE(b);
        x = ((a->ob_digit[size_a-1] << (2*PyLong_SHIFT-nbits)) |
             (a->ob_digit[size_a-2] << (PyLong_SHIFT-nbits)) |
             (a->ob_digit[size_a-3] >> nbits));

        y = ((size_b >= size_a - 2 ? b->ob_digit[size_a-3] >> nbits : 0) |
             (size_b >= size_a - 1 ? b->ob_digit[size_a-2] << (PyLong_SHIFT-nbits) : 0) |
             (size_b >= size_a ? b->ob_digit[size_a-1] << (2*PyLong_SHIFT-nbits) : 0));

        /* inner loop of Lehmer's algorithm; A, B, C, D never grow
        larger than PyLong_MASK during the algorithm. */
        A = 1; B = 0; C = 0; D = 1;
        for (k=0;; k++) {
            if (y-C == 0)
                break;
            q = (x+(A-1))/(y-C);
            s = B+q*D;
            t = x-q*y;
            if (s > t)
                break;
            x = y; y = t;
            t = A+q*C; A = D; B = C; C = (digit)s; D = (digit)t;
        }

        if (k == 0) {
            /* no progress; do a Euclidean step */
            if (Py_SIZE(b) == 0) {
                Py_DECREF(b);
                return a;
            }
            if (l_divmod(a, b, NULL, &d) < 0) {
                Py_DECREF(a);
                Py_DECREF(b);
                return NULL;
            }
            Py_DECREF(a);
            a = b;
            b = d;
            continue;
        }

        /*
          a, b = A*b-B*a, D*a-C*b if k is odd
          a, b = A*a-B*b, D*b-C*a if k is even
        */
        c = _PyLong_New(size_a);
        if (c == NULL) {
            Py_DECREF(a);
            Py_DECREF(b);
            return NULL;
        }

        d = _PyLong_New(size_a);
        if (d == NULL) {
            Py_DECREF(a);
            Py_DECREF(b);
            Py_DECREF(c);
            return NULL;
        }
        a_end = a->ob_digit + size_a;
        b_end = b->ob_digit + size_b;

        /* compute new a and new b in parallel */
        a_digit = a->ob_digit;
        b_digit = b->ob_digit;
        c_digit = c->ob_digit;
        d_digit = d->ob_digit;
        c_carry = 0;
        d_carry = 0;
        if (k&1) {
            while (b_digit < b_end) {
                c_carry += (A * *b_digit) - (B * *a_digit);
                d_carry += (D * *a_digit++) - (C * *b_digit++);
                *c_digit++ = (digit)(c_carry & PyLong_MASK);
                *d_digit++ = (digit)(d_carry & PyLong_MASK);
                c_carry >>= PyLong_SHIFT;
                d_carry >>= PyLong_SHIFT;
            }
            while (a_digit < a_end) {
                c_carry -= B * *a_digit;
                d_carry += D * *a_digit++;
                *c_digit++ = (digit)(c_carry & PyLong_MASK);
                *d_digit++ = (digit)(d_carry & PyLong_MASK);
                c_carry >>= PyLong_SHIFT;
                d_carry >>= PyLong_SHIFT;
            }
        }
        else {
            while (b_digit < b_end) {
                c_carry += (A * *a_digit) - (B * *b_digit);
                d_carry += (D * *b_digit++) - (C * *a_digit++);
                *c_digit++ = (digit)(c_carry & PyLong_MASK);
                *d_digit++ = (digit)(d_carry & PyLong_MASK);
                c_carry >>= PyLong_SHIFT;
                d_carry >>= PyLong_SHIFT;
            }
            while (a_digit < a_end) {
                c_carry += A * *a_digit;
                d_carry -= C * *a_digit++;
                *c_digit++ = (digit)(c_carry & PyLong_MASK);
                *d_digit++ = (digit)(d_carry & PyLong_MASK);
                c_carry >>= PyLong_SHIFT;
                d_carry >>= PyLong_SHIFT;
            }
        }
        assert(c_carry == 0);
        assert(d_carry == 0);

        Py_DECREF(a);
        Py_DECREF(b);
        a = long_normalize(c);
        b = long_normalize(d);
    }

    /* a fits into a long, so b must too */
    x = PyLong_AsLong((PyObject *)a);
    y = PyLong_AsLong((PyObject *)b);
    Py_DECREF(a);
    Py_DECREF(b);

    /* usual Euclidean algorithm for longs */
    while (y != 0) {
        t = y;
        y = x % y;
        x = t;
    }
    return (PyLongObject *)PyLong_FromLong(x);
}

PyObject *
_PyLong_GCD(PyObject *a, PyObject *b)
{
    long x, y, t;
    int overflow;

    x = PyLong_AsLongAndOverflow(a, &overflow);
    if (!overflow && !(x == -1 && PyErr_Occurred()) && x >= -LONG_MAX) {
        y = PyLong_AsLongAndOverflow(b, &overflow);
        if (!overflow && !(y == -1 && PyErr_Occurred()) && y >= -LONG_MAX) {
            /* Both a and b are small integers;
               use the usual gcd algorithm. */
            if (x < 0)
                x = -x;
            if (y < 0)
                y = -y;
            while (y != 0) {
                t = x % y;
                x = y;
                y = t;
            }
            return PyLong_FromLong(x);
        }
    }

    return (PyObject *)long_gcd((PyLongObject *)a, (PyLongObject *)b);
}
#else
#if PY_VERSION_HEX <= 0x030500A0
#define _PyLong_GCD(a, b) (NULL)
#endif
#endif
