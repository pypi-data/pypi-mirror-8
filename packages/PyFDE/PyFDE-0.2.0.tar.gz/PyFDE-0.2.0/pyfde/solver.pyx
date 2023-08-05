#cython: embedsignature=True, profile=True
'''Implements a differential evolution algorithm'''

import numpy as np
from numpy import random as rnd
from libc.stdlib cimport rand, RAND_MAX
cimport cython
cimport numpy as np

# fast random number generators
cdef int rand_int(int limit):
    cdef int divisor = RAND_MAX / limit
    cdef int retval = limit

    while retval == limit:
        retval = rand() / divisor

    return retval

cdef double rand_double():
    return float(rand()) / RAND_MAX

cdef sample3(int n_pop):
    r1 = rand_int(n_pop)
    r2 = rand_int(n_pop)
    r3 = rand_int(n_pop)

    while r2 == r1: r2 = rand_int(n_pop)
    while r3 == r1 or r3 == r2: r3 = rand_int(n_pop)

    return r1, r2, r3

cdef class Solver:
    '''

    Computational state of the optimization procedure. Holds the vector
    population, fitness evaluations, and the parameters.

    Parameters
    ----------
    fitness : function
        Fitness evaluation function to be used. Must accept a double array
        as parameter and return the fitness evaluation as a float
    n_dim: int
        Number of dimensions
    n_pop: int
        Number of vectors in the population
    limits: tuple (min, max) or list of tuples [(min, max), ...]
        Limits for the search space dimension. If it is a tuple, then every
        dimension will have the same limits. If it is a list, then each
        dimension will have the corresponding list element limit.
    '''

    cdef public double f
    '''Differential weight, in the [0., 2.] range'''

    cdef public double cr
    '''Crossover rate, in the [0., 1.] range'''

    cdef pop, trial, fit, trial_fit, fitness
    cdef list limits

    def __init__(self, fitness, n_dim, n_pop=30, limits=(-1.,1.)):
        self.fitness = fitness
        self.f = 0.7
        self.cr = 0.95

        if type(limits) is tuple:
            self.limits = [limits]*n_dim
        else:
            self.limits = limits

        assert len(self.limits) == n_dim

        self.prepare(n_pop)

    def prepare(self, n_pop=None):
        '''Resets the solver internal state for a new computation.

        Can be called to reuse an existing Solver instance.

        Parameters
        ----------
        n_pop : int or None
            Number of vectors in the population. If None, will use the current
            number of vectors.
        '''
        n_pop, n_dim = n_pop or self.pop.shape[0], len(self.limits)
        self.pop = np.empty( (n_pop, n_dim) )
        self.trial = np.empty( (n_pop, n_dim) )

        for dim in range(n_dim):
            lower, upper = self.limits[dim]
            self.pop[:, dim] = rnd.uniform(lower, upper, n_pop)

        self.fit, self.trial_fit = np.zeros(n_pop), np.zeros(n_pop)
        self.evaluate(self.pop, self.fit)

    def generate_trial(self):
        '''Generates a new trial population by using the current vectors.'''
        cdef:
            double[:,::1] pop, trial
            double val
            int n_pop, n_dim, r0, r1, r2, always, p, d

        pop, trial, limits = self.pop, self.trial, self.limits
        n_pop, n_dim = pop.shape[0], pop.shape[1]

        for p in range(n_pop):
            r0, r1, r2 = sample3(n_pop)
            always = rand_int(n_dim)

            for d in range(n_dim):
                if rand_double() < self.cr or d == always:
                    val = pop[r0][d] + self.f*(pop[r1][d]-pop[r2][d])
                else:
                    val = pop[p][d]

                trial[p][d] = max(limits[d][0], min(limits[d][1], val))

    def evaluate(self, double[:,::1] pop, double[::1] fit):
        '''Evaluates a population, storing their fitness for later use.

        Parameters
        ----------
        pop : double[n_pop,n_dim]
            Population to evaluate
        fit : double[n_pop]
            Location to store the fitness evaluations

        '''
        cdef int ind
        for ind in range(pop.shape[0]):
            fit[ind] = self.fitness(pop[ind])

    def selection(self):
        '''Merges the best trial vectors to the main population'''
        cdef:
            double[:,::1] pop, trial
            double[::1] fit, trial_fit
            int p

        pop, trial = self.pop, self.trial
        fit, trial_fit = self.fit, self.trial_fit

        for p in range(self.pop.shape[0]):
            if trial_fit[p] > fit[p]:
                fit[p] = trial_fit[p]
                pop[p] = trial[p]

    def step(self):
        '''Performs one iteration of the optimization algorithm.'''
        self.generate_trial()
        self.evaluate(self.trial, self.trial_fit)
        self.selection()

    def run(self, int n_it=1000):
        '''Runs the optimization algorithm for a number of iterations.

        Parameters
        ----------
        n_it : int
            Number of iterations to be performed

        Returns
        -------
        (double[n_dim], float)
            Returns a tuple with the best solution and its fitness evaluation

        '''
        cdef int besti

        for _ in range(n_it):
            self.step()

        besti = np.argmax(self.fit)
        return self.pop[besti], self.fit[besti]

    def __call__(self, int n_it=1):
        '''Returns a generator that can be used for writing custom stopping
        conditions.

        Parameters
        ----------
        n_it : int
            Number of iterations to perform before yielding the current
            solution

        Returns
        -------
        generator
            Returns a generator that yields the current best solution and its
            fitness value
        '''
        while True:
            yield self.run(n_it)

    def __iter__(self):
        '''Iterates through every vector in the population

        Returns
        -------
        iterator:
            Returns a (vector, fitness) iterator
        '''
        cdef int p
        for p in range(self.pop.shape[0]):
            yield self.pop[p], self.fit[p]