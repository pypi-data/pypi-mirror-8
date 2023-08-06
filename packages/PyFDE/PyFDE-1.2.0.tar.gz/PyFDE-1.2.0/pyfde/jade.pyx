#cython: embedsignature=True, boundscheck=False, wraparound=False, cdivision=True

cimport numpy as np
cimport classicde
import numpy as np

from classicde cimport ClassicDE
from classicde cimport clip
from rng cimport Random

cdef class JADE(ClassicDE):
    """
    Implementation of the adaptative DE algorithm proposed by Zhang, J.
    et al, JADE: Adaptive Differential Evolution with Optional External
    Archive.

    See pyfde.ClassicDE constructor for the constructor parameters.
    """

    cdef public double p
    """
    Parameter between 0 and 1 that determined the top `p` of the
    population were the best vector will be selected to guide the optimization
    procedure.
    """

    cdef public double c
    """
    Parameter between 0 and 1 that controls the rate of the adaptation of
    the CR and F parameters.
    """

    cdef cr_arr, f_arr

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # JADE parameters
        self.p = 0.1
        self.c = 0.1

        # current means (u_cr and u_f in the literature)
        self.cr = 0.5
        self.f = 0.5

    def prepare(self, new_pop=None):
        """
        Resets the solver internal state for a new computation.
        Can be called to reuse an existing solver instance.

        Parameters
        ----------
        new_pop : int or None
            New number of vectors in the population. If None, will use the
            current number of vectors.
        """
        cdef:
            int n_pop

        super().prepare(new_pop)
        n_pop = self.pop.shape[0]
        self.cr_arr = np.empty(n_pop)
        self.f_arr = np.empty(n_pop)

    def generate_trial(self):
        """
        Generates a new trial population by using the current vectors.

        This method differs from the base implementation in two points:
        
        * The random vector selected to guide the optimization procedure is
          selected from the top `p` vectors (bias towards better fitness).
        * The CR and F parameters are computed per vector, and are fluctuations
          around the mean CR and mean F adaptative parameters.

        The original JADE algorithm can also be implemented with an archive,
        that can enhance the performance of the algorithm in high dimentional
        cases. This implementations *does not* includes this archive.

        """
        cdef:
            double[:,::1] pop = self.pop, trial = self.trial, limits = self.limits
            double val, cr_i, f_i
            int n_pop = pop.shape[0], n_dim = pop.shape[1], r1, r2, always, p, d, pbest_i
            Random rng = self.rng

        # clear the cache
        self.k_high = None 

        for i in range(n_pop):
            r1 = rng.rand_int(n_pop)
            r2 = rng.rand_int(n_pop)
            while r1 == i: r1 = rng.rand_int(n_pop)
            while r2 == r1 or r2 == i: r2 = rng.rand_int(n_pop)
            
            always = rng.rand_int(n_dim)
            pbest_i = self.best_k(int(self.p * n_pop))

            cr_i = clip(0.0, 1.0, self.rng.randn(self.cr, 0.1))
            f_i = 0.0
            while f_i <= 0.0:
                f_i = clip(0.0, 1.0, self.rng.randc(self.f, 0.1))
            self.cr_arr[i] = cr_i
            self.f_arr[i] = f_i

            for d in range(n_dim):
                if rng.rand_double() < cr_i or d == always:
                    val = (pop[i, d] +
                           f_i*(pop[pbest_i, d] - pop[i, d]) +
                           f_i*(pop[r1, d] - pop[r2, d]))
                else:
                    val = pop[i, d]

                trial[i, d] = clip(limits[d, 0], limits[d, 1], val)

    def selection(self):
        """Merges the best trial vectors to the main population."""
        cdef:
            double[:,::1] pop = self.pop, trial = self.trial
            double[::1] fit = self.fit, trial_fit = self.trial_fit
            double[::1] cr_arr = self.cr_arr, f_arr = self.f_arr
            double num_cr=0.0, den_cr=0.0, num_f=0.0, den_f=0.0
            int i

        for i in range(self.pop.shape[0]):
            if trial_fit[i] > fit[i]:
                # place new vector
                fit[i] = trial_fit[i]
                pop[i] = trial[i]

                # update the running arithmethic and lehmer means
                num_cr += cr_arr[i]
                den_cr += 1.0

                num_f += f_arr[i]**2
                den_f += f_arr[i]

        # update the mean values of CR and F
        if den_cr > 0:
            self.cr = (1.0-self.c)*self.cr + self.c*(num_cr/den_cr)
        
        if den_f > 0:
            self.f = (1.0-self.c)*self.f + self.c*(num_f/den_f)

    def __repr__(self):
        return 'JADE(n_dim={}, n_pop={})'.format(*self.pop.shape)

