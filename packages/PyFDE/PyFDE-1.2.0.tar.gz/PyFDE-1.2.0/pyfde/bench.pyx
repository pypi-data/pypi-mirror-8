#cython: embedsignature=True, boundscheck=False, wraparound=False, cdivision=True
"""Implements some common benchmark functions."""
from libc.math cimport sin, cos, sqrt, fabs, M_PI

cdef schewefel_c(double[::1] p):
    cdef double sum = 0.
    cdef int i

    for i in range(p.shape[0]):
        sum += p[i]*sin(sqrt(fabs(p[i])))

    return sum

def schewefel(double[::1] p):
    """Schewefel function

    Parameters
    ----------
    p : double[n_dim]
        Array with the coefficients

    Returns
    -------
    float
        Function value at p
    """
    return schewefel_c(p)

def schewefel_batch(double[:,::1] pop, double[::1] fit):
    """Batch version of the Schewefel function.
    
    Parameters
    ----------
    pop : double[n_pop, n_dim]
        Array with the population to be evaluated
    fit : double[n_pop]
        Array to write the fitness evaluations to
    """
    for i in range(pop.shape[0]):
        fit[i] = schewefel_c(pop[i])

def rastrigin(double[::1] p):
    """Rastrigin function.

    Parameters
    ----------
    p : double[n_dim]
        Array with the coefficients

    Returns
    -------
    float
        Function value at p
    """
    x, y = p[0], p[1]
    return 20 + (x**2 - 10*cos(2*M_PI*x)) + (y**2 - 10*cos(2*M_PI*y))
