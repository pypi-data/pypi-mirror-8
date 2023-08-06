#cython: embedsignature=True, boundscheck=False, wraparound=False, cdivision=True

"""Implements a differential evolution algorithm"""
import numpy as np
cimport numpy as np
from rng cimport Random

cimport classicde
from classicde cimport classicde

import time

cdef inline double clip(double min_, double max_, double val):
    return max(min_, min(max_, val))

cdef class ClassicDE:

    def __init__(self, fitness, n_dim, n_pop=30, limits=(-1., 1.), batch=False, seed=None):
        assert fitness
        assert n_dim > 0
        assert n_pop > 3

        if seed is None:
            seed = max(1, int(time.time() * 1e6))
       
        assert seed > 0

        self.fitness = fitness
        self.f = 0.7
        self.cr = 0.95

        self.batch = batch

        self.rng = Random(seed)

        if type(limits) is tuple:
            limits = [limits]*n_dim

        self.limits = np.array(limits, dtype=np.double)
        assert self.limits.shape == (n_dim, 2)

        self.prepare(n_pop)

    def prepare(self, new_pop=None):
        """Resets the solver internal state for a new computation.

        Can be called to reuse an existing solver instance.

        Parameters
        ----------
        new_pop : int or None
            New number of vectors in the population. If None, will use the
            current number of vectors.
        """
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
                self.pop[ind, dim] = self.rng.rand_double() * range_ + lower

        self.fit = np.zeros(n_pop)
        self.trial_fit = np.zeros(n_pop)
        self.evaluate(self.pop, self.fit)

    def generate_trial(self):
        """Generates a new trial population by using the current vectors."""
        cdef:
            double[:,::1] pop = self.pop, trial = self.trial, limits = self.limits
            double val
            int n_pop = pop.shape[0], n_dim = pop.shape[1], r0, r1, r2, always, p, d
            Random rng = self.rng

        for p in range(n_pop):
            r0 = rng.rand_int(n_pop)
            r1 = rng.rand_int(n_pop)
            r2 = rng.rand_int(n_pop)
            while r1 == r0: r1 = rng.rand_int(n_pop)
            while r2 == r0 or r2 == r1: r2 = rng.rand_int(n_pop)

            always = rng.rand_int(n_dim)

            for d in range(n_dim):
                if rng.rand_double() < self.cr or d == always:
                    val = pop[r0, d] + self.f*(pop[r1, d]-pop[r2, d])
                else:
                    val = pop[p, d]

                trial[p, d] = max(limits[d, 0], min(limits[d, 1], val))

    def evaluate(self, double[:,::1] pop, double[::1] fit):
        """Evaluates a population, storing their fitness for later use.

        Parameters
        ----------
        pop : double[n_pop,n_dim]
            Population to evaluate
        fit : double[n_pop]
            Location to store the fitness evaluations

        """
        cdef int ind

        # better than patching evaluate on the run...
        if self.batch:
            self.fitness(pop, fit)
        else:
            for ind in range(pop.shape[0]):
                fit[ind] = self.fitness(pop[ind])

    def selection(self):
        """Merges the best trial vectors to the main population."""
        cdef:
            double[:,::1] pop = self.pop, trial = self.trial
            double[::1] fit = self.fit, trial_fit = self.trial_fit
            int p

        for p in range(self.pop.shape[0]):
            if trial_fit[p] > fit[p]:
                fit[p] = trial_fit[p]
                pop[p] = trial[p]

    def step(self):
        """Performs one iteration of the optimization algorithm."""
        self.generate_trial()
        self.evaluate(self.trial, self.trial_fit)
        self.selection()

    def best_k(self, int k):
        """Returns the index of a random vector from the `k` vectors with
        the highest fitness. If `k` is equal to one, then the best vector
        index is returned deterministically.

        The sorted indexes are cached to optimize the common case where this
        function can be called multiple times with the same fitness array.

        Parameters
        ----------
        k : int
            Size of the group with the best fitness values

        Returns
        -------
        int : int
            Index of the choosen vector
        """
        if k < 2:
            return np.argmax(self.fit)

        if self.k_high is None:
            self.k_high = np.argsort(self.fit)[:-k-1:-1]

        idx = self.rng.rand_int(k)
        return self.k_high[idx]

    def run(self, int n_it=1000):
        """Runs the optimization algorithm for a number of iterations.

        Parameters
        ----------
        n_it : int
            Number of iterations to be performed

        Returns
        -------
        (double[n_dim], float)
            Returns a tuple with the best solution and its fitness evaluation

        """
        cdef int besti

        for _ in range(n_it):
            self.step()

        besti = self.best_k(1)
        return self.pop[besti], self.fit[besti]

    def __call__(self, int n_it=1):
        """Returns a generator that can be used for writing custom stopping
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
        """
        while True:
            yield self.run(n_it)

    def __iter__(self):
        """Iterates through every vector in the population

        Returns
        -------
        iterator:
            Returns a (vector, fitness) iterator
        """
        cdef int p
        for p in range(self.pop.shape[0]):
            yield self.pop[p], self.fit[p]

    def __repr__(self):
        return 'ClassicDE(n_dim={}, n_pop={})'.format(*self.pop.shape)
