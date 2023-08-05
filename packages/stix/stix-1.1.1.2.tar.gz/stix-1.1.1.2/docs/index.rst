python-stix |release| Documentation
===================================

The **python-stix** library provides an API for developing and consuming *Structured Threat Information eXpression* (**STIX**) content. Developers can leverage the API to develop applications that create, consume, translate, or otherwise process STIX content. This page should help new developers get started with using this library. For more information about STIX, please refer to the `STIX website`_.

.. note::

	These docs provide standard reference for this Python library. For documentation on *idiomatic* usage and *common patterns*, as well as various STIX-related information and utilities, please visit the `STIXProject at GitHub`_.
	
	.. _STIXProject at GitHub: http://stixproject.github.io/

.. _STIX website: http://stix.mitre.org

Versions
--------
Each version of python-stix is designed to work with a single version of the
STIX Language.  The table below shows the latest version the library for each
version of STIX.

============ ===================
STIX Version python-stix Version
============ ===================
1.1.1        1.1.1.1 (`PyPI`__) (`GitHub`__)
1.1.0        1.1.0.6 (`PyPI`__) (`GitHub`__)
1.0.1        1.0.1.1 (`PyPI`__) (`GitHub`__)
1.0          1.0.0a7 (`PyPI`__) (`GitHub`__)
============ ===================

__ https://pypi.python.org/pypi/stix/1.1.1.1
__ https://github.com/STIXProject/python-stix/tree/v1.1.1.1
__ https://pypi.python.org/pypi/stix/1.1.0.6
__ https://github.com/STIXProject/python-stix/tree/v1.1.0.6
__ https://pypi.python.org/pypi/stix/1.0.1.1
__ https://github.com/STIXProject/python-stix/tree/v1.0.1.1
__ https://pypi.python.org/pypi/stix/1.0.0a7
__ https://github.com/STIXProject/python-stix/tree/v1.0.0a7


Contents
--------
.. toctree::
   :maxdepth: 2

   installation
   getting_started
   examples/index
   api_vs_bindings/index

API Coverage
============
Want to find out which STIX constructs the *python-stix* APIs currently cover? Check here for a current overview!

.. toctree::
   :maxdepth: 1
   
   api/coverage

API Reference
=============

.. toctree::
   :maxdepth: 1

   api/index
   
Bindings Reference
==================

.. toctree::
   :maxdepth: 1

   binding/index

Contributing
============
If a bug is found, a feature is missing, or something just isn't behaving the way you'd expect it to, please submit an issue to our `tracker`_. If you'd like to contribute code to our repository, you can do so by issuing a `pull request`_ and we will work with you to try and integrate that code into our repository.

.. _tracker: https://github.com/STIXProject/python-stix/issues
.. _pull request: https://help.github.com/articles/using-pull-requests

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

