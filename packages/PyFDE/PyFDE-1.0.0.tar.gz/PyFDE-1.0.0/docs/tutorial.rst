PyFDE tutorial
==============

In this tutorial we will write a program to find (we hope so) the global
minima of the 2D Rastrigin function given by Eq. :eq:`rast`:

.. math::
    :label: rast

    f(x,y) = 20 + (x^2 - 10\cos(2\pi x)) + (y^2 - 10\cos(2\pi y))

Eq. :eq:`rast` has a global minimum at *(x=0,y=0)*. Our program will use
**PyFDE**, starting by loading the required modules:

.. code-block:: python

    import pyfde
    from math import cos, pi

The next step is to define the *fitness evaluation function*. This function
receives one list containing the description of a vector (in this case an
array with two floats), and must return the fitness evaluation, as a float.
This fitness value represents the quality of the solution (the higher the
better), and will guide the optimization process.

We want to minimize the value of the Rastrigin function, so our fitness
evaluation will be the output of the function multiplied by -1. Thus, when the
output of the function decrease, our fitness evaluation increases:

.. code-block:: python

    def fitness(p):
        x, y = p[0], p[1]
        val = 20 + (x**2 - 10*cos(2*pi*x)) + (y**2 - 10*cos(2*pi*y))
        return -val

With the function defined, we can now initialize the solver state and
configure its parameters:

.. code-block:: python

    solver = pyfde.Solver(fitness, n_dim=2, n_pop=40, limits=(-5.12, 512))
    solver.cr, solver.f = 0.9, 0.45

We used a population of 40 vectors in a 2D search space (one for each
variable, x and y). We have limited the search space to values between
(-5.12, 5.12). We can also configure the limits of each dimension manually by
passing a list of tuples, like *limits=[(-5.12, 5.12), (-2.5, 2.5)]*.

Lets run it:

.. code-block:: python

    best, fit = solver.run(n_it=150)

Now, the best found solution is available by acessing *best[0]* and
*best[1]*. The final fitness evaluation is stored in *fit*.

Finally, let's print the solution:

.. code-block:: python

    print("**Best solution found**")
    print("x, y    = {:.2f}, {:.2f} (expected: 0.00, 0.00)".format(best[0], best[1]))
    print("Fitness = {:.2f}".format(fit))

The whole source code is available at *tests/rastrigin.py*.

Iterators
---------

To use custom stopping conditions, one can use the generator syntax:

.. code-block:: python

    for best, fit in solver(n_it=10):
        # custom logic here, breaking when desired

It is also possible to access every solution vector by iterating the solver:

.. code-block:: python

    for vector, fit in solver:
        print(vector, fit)

Batch mode
----------

To further enhance the performance, specially if the fitness function is also
implemented in Cython, it is possible to specify a `batch` mode by setting
the `batch` parameter to True in the solver constructor.

In 'batch' mode, the fitness function will be called only once per iteration
to evaluate the fitness of all the population. In this mode, the fitness
function will receive the population as first parameter, and the fitness
array to be updated as second parameter: `fitness(double[:,::1] pop,
double[::1] fit)`.
