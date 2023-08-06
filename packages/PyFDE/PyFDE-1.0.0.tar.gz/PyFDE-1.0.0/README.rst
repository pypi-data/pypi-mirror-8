PyFDE
=====

.. image:: https://api.shippable.com/projects/54294a2980088cee586cfc7d/badge?branchName=master
.. image:: https://pypip.in/version/PyFDE/badge.png?style=flat
    :target: https://pypi.python.org/pypi/PyFDE
    :alt: Latest Version

PyFDE is an implementation of differential evolution for Python 3. Its main
focus is ease of use and performance. The core optimization procedure was
implemented in Cython for performance.

The documentation is available at http://pythonhosted.org/PyFDE .

Installation
------------

To install PyFDE from the source package, run:

.. code-block:: bash
    
    python setup.py install
    
PyFDE targets Python 3.4 and depends on NumPy at compile/run time. Cython is
only needed when changing the library itself (needed for generating the C
modules). Optionally, one can implement the fitness function in Cython for
performance too.

Contribute
----------

- Source Code: https://bitbucket.org/lucashnegri/pyfde
- Issues: https://bitbucket.org/lucashnegri/pyfde/issues
- Direct contact: Lucas Hermann Negri - lucashnegri <at> gmail.com

License
-------

The project is licensed under the MIT license.
