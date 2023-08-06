#cython: embedsignature=True, boundscheck=False, wraparound=False, cdivision=True

'''Implements a differential evolution algorithm'''

from numpy import random as rnd
from libc.stdlib cimport rand, RAND_MAX
import numpy as np
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

cdef class Solver:
    '''

    Computational state of the optimization procedure. Holds the vector
    population, fitness evaluations, and the parameters.

    Parameters
    ----------
    fitness : function
        Fitness evaluation function to be used. Must accept a double array
        as parameter and return the fitness evaluation as a float.

        Alternatively (by using batch=True), it can be a function that accepts
        two parameters: a double[n_pop, n_dim] corresponding to the population
        to be evaluated and a double[n_pop], correponding to where the fitness
        evaluations must be written to.
        
    n_dim: int, > 0
        Number of dimensions
    n_pop: int, > 3
        Number of vectors in the population
    limits: tuple (min, max), list of tuples or double[n_dim][2]
        Limits for the search space dimension. If it is a tuple, then every
        dimension will have the same limits. If it is a list of tuples or an
        array, then each dimension will have the corresponding limit.
    batch: bool
        If the `batch` mode should be used.
    '''

    cdef public double f
    '''Differential weight, in the [0., 2.] range'''

    cdef public double cr
    '''Crossover rate, in the [0., 1.] range'''

    cdef pop, trial, fit, trial_fit, fitness, limits
    cdef bint batch

    def __init__(self, fitness, n_dim, n_pop=30, limits=(-1.,1.), batch=False):
        assert fitness
        assert n_dim > 0
        assert n_pop > 3

        self.fitness = fitness
        self.f = 0.7
        self.cr = 0.95

        self.batch = batch

        if type(limits) is tuple:
            limits = [limits]*n_dim

        self.limits = np.array(limits, dtype=np.double)
        assert self.limits.shape == (n_dim, 2)

        self.prepare(n_pop)

    def prepare(self, new_pop=None):
        '''Resets the solver internal state for a new computation.

        Can be called to reuse an existing Solver instance.

        Parameters
        ----------
        new_pop : int or None
            New number of vectors in the population. If None, will use the current
            number of vectors.
        '''
        cdef:
            int n_pop, n_dim
            double range_, lower, upper

        n_pop = new_pop or self.pop.shape[0]
        n_dim = len(self.limits)
        self.pop = np.empty((n_pop, n_dim))
        self.trial = np.empty((n_pop, n_dim))

        # random initialization
        for dim in range(n_dim):
            lower, upper = self.limits[dim]
            range_ = upper - lower

            for ind in range(n_pop):
                self.pop[ind, dim] = rand_double() * range_ + lower

        self.fit = np.zeros(n_pop)
        self.trial_fit = np.zeros(n_pop)
        self.evaluate(self.pop, self.fit)

    def generate_trial(self):
        '''Generates a new trial population by using the current vectors.'''
        cdef:
            double[:,::1] pop, trial, limits
            double val
            int n_pop, n_dim, r0, r1, r2, always, p, d

        pop, trial, limits = self.pop, self.trial, self.limits
        n_pop, n_dim = pop.shape[0], pop.shape[1]

        for p in range(n_pop):
            r0 = rand_int(n_pop)
            r1 = rand_int(n_pop)
            r2 = rand_int(n_pop)
            while r1 == r0: r1 = rand_int(n_pop)
            while r2 == r0 or r2 == r1: r2 = rand_int(n_pop)

            always = rand_int(n_dim)

            for d in range(n_dim):
                if rand_double() < self.cr or d == always:
                    val = pop[r0, d] + self.f*(pop[r1, d]-pop[r2, d])
                else:
                    val = pop[p, d]

                trial[p, d] = max(limits[d, 0], min(limits[d, 1], val))

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

        # better than patching evaluate on the run...
        if self.batch:
            self.fitness(pop, fit)
        else:
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

    def __repr__(self):
        return 'Solver(fitness, n_dim={}, n_pop={})'.format(*self.pop.shape)
