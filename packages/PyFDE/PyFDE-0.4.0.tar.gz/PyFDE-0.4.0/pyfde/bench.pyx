#cython: embedsignature=True, boundscheck=False, wraparound=False, cdivision=True
'''Implements some common benchmark functions.'''
from libc.math cimport sin, cos, sqrt, M_PI

def schewefel(double[::1] p):
    '''Schewefel function

    Parameters
    ----------
    p : double[n_dim]
        Array with the coefficients

    Returns
    -------
    float
        Function value at p
    '''
    cdef double sum = 0.
    cdef int i

    for i in range(p.shape[0]):
        sum += p[i]*sin(sqrt(abs(p[i])))

    return sum

def rastrigin(double[::1] p):
    '''Rastrigin function.

    Parameters
    ----------
    p : double[n_dim]
        Array with the coefficients

    Returns
    -------
    float
        Function value at p
    '''
    x, y = p[0], p[1]
    return 20 + (x**2 - 10*cos(2*M_PI*x)) + (y**2 - 10*cos(2*M_PI*y))
