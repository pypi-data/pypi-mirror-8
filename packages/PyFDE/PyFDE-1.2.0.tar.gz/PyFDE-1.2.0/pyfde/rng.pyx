#cython: embedsignature=True, boundscheck=False, wraparound=False, cdivision=True

from libc.math cimport log, tan, exp, sqrt, M_PI
cimport rng
from rng cimport *

cdef double CONST = 4 * exp(-0.5) / sqrt(2.0)

cdef extern from "limits.h":
    enum: ULLONG_MAX

cdef uint64_t RAND_MAX = ULLONG_MAX

cdef class Random:
    def __init__(self, seed=42):
        """Constructor. Accepts an initial seed."""
        self.rand_seed(seed)

    cpdef rand_seed(self, uint64_t x):
        """Initializes the internal state with a 64 bit integer by using
        two passes of the MurmurHash3.
        
        Parameters
        ----------
        x : uint64_t
            Seed to initialize the internal state. Determines the future
            outputs of the generator. Should be greater than zero.
        """
        for i in range(2):
            x ^= x >> 33
            x *= 0xff51afd7ed558ccdULL
            x ^= x >> 33
            x *= 0xc4ceb9fe1a85ec53ULL
            x ^= x >> 33
            self.s[i] = x

    cpdef uint64_t rand(self):
        """Generates a 64bit random int.""" 
        cdef:
            uint64_t s0 = self.s[1], s1 = self.s[0]

        self.s[0] = s0
        s1 ^= s1 << 23
        self.s[1] = s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26)
        return self.s[1] + s0

    
    cpdef uint64_t rand_int(self, uint64_t limit):
        """Generates a random integer."""
        cdef uint64_t divisor = RAND_MAX // limit 
        cdef uint64_t retval = limit

        while retval == limit:
            retval = self.rand() // divisor

        return retval
  

    cpdef double rand_double(self):
        """Generates a random double."""
        return float(self.rand()) / RAND_MAX


    cpdef double randn(self, double mu, double sigma):
        """Normal RNG."""
        cdef double u1, u2, z

        while True:
            u1 = self.rand_double()
            u2 = 1.0 - self.rand_double()
            z = CONST * (u1 - 0.5) / u2

            if z*z/4.0 <= -log(u2):
                break

        return mu + z*sigma


    cpdef double randc(self, double mu, double sigma):
        """Cauchy RNG."""
        cdef double p = 0.0

        while p == 0.0:
            p = self.rand_double()

        return mu + sigma * tan(M_PI * (p - 0.5))
