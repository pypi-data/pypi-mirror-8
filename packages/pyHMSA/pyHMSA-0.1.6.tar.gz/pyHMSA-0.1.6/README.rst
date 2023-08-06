pyHMSA
======

.. image:: https://pypip.in/version/pyHMSA/badge.svg
   :target: https://pypi.python.org/pypi/pyHMSA/
   :alt: Latest Version

.. image:: https://pypip.in/implementation/pyHMSA/badge.svg
   :target: https://pypi.python.org/pypi/pyHMSA/
   :alt: Supported Python implementations
   
.. image:: https://pypip.in/py_versions/pyHMSA/badge.svg
   :target: https://pypi.python.org/pypi/pyHMSA/
   :alt: Supported Python versions

.. image:: https://pypip.in/wheel/pyHMSA/badge.svg
   :target: https://pypi.python.org/pypi/pyHMSA/
   :alt: Wheel Status

.. image:: https://pypip.in/license/pyHMSA/badge.svg
   :target: https://pypi.python.org/pypi/pyHMSA/
   :alt: License

.. image:: https://readthedocs.org/projects/pyhmsa/badge/?version=latest
   :target: https://readthedocs.org/projects/pyhmsa/

.. image:: https://travis-ci.org/pyhmsa/pyhmsa.svg?branch=master
   :target: https://travis-ci.org/pyhmsa/pyhmsa
   
.. image:: https://codecov.io/github/pyhmsa/pyhmsa/coverage.svg?branch=master
   :target: https://codecov.io/github/pyhmsa/pyhmsa?branch=master

pyHMSA is a pure Python implementation of the MSA / MAS / AMAS HyperDimensional 
Data File (HMSA, for short) specifications. 
This file format is intended to be a common exchange format for microscopy and 
microanalysis data. 
More information about the file format and its specifications can be found 
`here <http://www.csiro.au/luminescence/HMSA/index.html>`_.

The library is designed to be minimalist, leaving post-processing of the data
to the user's script.
The only dependency of pyHMSA is to `NumPy <http://www.numpy.org>`_, in order
to represent the multi-dimensional data.

pyHMSA is written to support both Python 2 and 3.

The library is provided under the MIT license.

More information can be found at the website:

http://pyhmsa.readthedocs.org

The most current development version is always available from our
GitHub repository:

https://github.com/pyhmsa/pyhmsa