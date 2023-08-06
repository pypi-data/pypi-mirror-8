#cython: embedsignature=True, boundscheck=False, wraparound=False, cdivision=True

"""Implements a differential evolution algorithm"""
import numpy as np
cimport numpy as np

cdef extern from "limits.h":
    enum: ULLONG_MAX

ctypedef unsigned long long uint64_t
cdef uint64_t RAND_MAX = ULLONG_MAX

cdef class XorShift:
    """A fast pseudo random number generator."""
    cdef uint64_t s[2]

    def __init__(self, seed=42):
        self.rand_seed(seed)

    cdef rand_seed(self, uint64_t x):
        """Initializes the internal state with a 64 bit integer by using
        two passes of the MurmurHash3.
        
        Parameters
        ----------
        x : uint64_t
            Seed to initialize the internal state. Determines the future
            outputs of the generator.
        """
        for i in range(2):
            x ^= x >> 33
            x *= 0xff51afd7ed558ccdULL
            x ^= x >> 33
            x *= 0xc4ceb9fe1a85ec53ULL
            x ^= x >> 33
            self.s[i] = x

    cdef uint64_t rand(self):
        """Generates a 64bit random int.""" 
        cdef:
            uint64_t s0 = self.s[1], s1 = self.s[0]

        self.s[0] = s0
        s1 ^= s1 << 23
        self.s[1] = s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26)
        return self.s[1] + s0

    cdef uint64_t rand_int(self, uint64_t limit):
        cdef uint64_t divisor = RAND_MAX // limit 
        cdef uint64_t retval = limit

        while retval == limit:
            retval = self.rand() // divisor

        return retval
   
    cdef double rand_double(self):
        return float(self.rand()) / RAND_MAX

cdef class Solver:
    """
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
    n_dim : int, > 0
        Number of dimensions
    n_pop : int, > 3
        Number of vectors in the population
    limits : tuple (min, max), list of tuples or double[n_dim][2]
        Limits for the search space dimension. If it is a tuple, then every
        dimension will have the same limits. If it is a list of tuples or an
        array, then each dimension will have the corresponding limit.
    batch : bool
        If the `batch` mode should be used.
    seed : int 
        Seed used to initialize the pseudo random number generator.
    """

    cdef public double f
    """Differential weight, in the [0., 2.] range"""

    cdef public double cr
    """Crossover rate, in the [0., 1.] range"""

    cdef pop, trial, fit, trial_fit, fitness, limits
    cdef bint batch

    cdef XorShift rng

    def __init__(self, fitness, n_dim, n_pop=30, limits=(-1.,1.), batch=False, seed=42):
        assert fitness
        assert n_dim > 0
        assert n_pop > 3

        self.fitness = fitness
        self.f = 0.7
        self.cr = 0.95

        self.batch = batch
        self.rng = XorShift(seed)

        if type(limits) is tuple:
            limits = [limits]*n_dim

        self.limits = np.array(limits, dtype=np.double)
        assert self.limits.shape == (n_dim, 2)

        self.prepare(n_pop)

    def prepare(self, new_pop=None):
        """Resets the solver internal state for a new computation.

        Can be called to reuse an existing Solver instance.

        Parameters
        ----------
        new_pop : int or None
            New number of vectors in the population. If None, will use the current
            number of vectors.
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
            XorShift rng = self.rng

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
        """Merges the best trial vectors to the main population"""
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

        besti = np.argmax(self.fit)
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
        return 'Solver(fitness, n_dim={}, n_pop={})'.format(*self.pop.shape)
