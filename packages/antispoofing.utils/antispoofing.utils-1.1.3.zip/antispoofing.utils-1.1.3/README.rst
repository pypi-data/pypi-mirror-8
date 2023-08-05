===============================================================================
Utilitary package for antispoofing countermeasures
===============================================================================

This package contains some utility functions to be used in antispoofing countermeasures codes. The goal of this package is to centralize some functions in commom. This package contains:
  - LDA Machine
  - PCA Machine
  - Function to normalize parameters
  - Performance measure functions
  - Eyes localization function


If you use this package and/or its results, please cite the following publications:

1. Bob as the core framework used to run the experiments::

    @inproceedings{Anjos_ACMMM_2012,
      author = {A. Anjos AND L. El Shafey AND R. Wallace AND M. G\"unther AND C. McCool AND S. Marcel},
      title = {Bob: a free signal processing and machine learning toolbox for researchers},
      year = {2012},
      month = oct,
      booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
      publisher = {ACM Press},
    }


Installation
------------

.. note:: 

  If you are reading this page through our GitHub portal and not through PyPI,
  note **the development tip of the package may not be stable** or become
  unstable in a matter of moments.

  Go to `http://pypi.python.org/pypi/antispoofing.utils
  <http://pypi.python.org/pypi/antispoofing.utils>`_ to download the latest
  stable version of this package.

There are 2 options you can follow to get this package installed and
operational on your computer: you can use automatic installers like `pip
<http://pypi.python.org/pypi/pip/>`_ (or `easy_install
<http://pypi.python.org/pypi/setuptools>`_) or manually download, unpack and
use `zc.buildout <http://pypi.python.org/pypi/zc.buildout>`_ to create a
virtual work environment just for this package.

Using an automatic installer
============================

Using ``pip`` is the easiest (shell commands are marked with a ``$`` signal)::

  $ pip install antispoofing.utils

You can also do the same with ``easy_install``::

  $ easy_install antispoofing.utils

This will download and install this package plus any other required
dependencies. It will also verify if the version of Bob you have installed
is compatible.

This scheme works well with virtual environments by `virtualenv
<http://pypi.python.org/pypi/virtualenv>`_ or if you have root access to your
machine. Otherwise, we recommend you use the next option.

Using ``zc.buildout``
=====================

Download the latest version of this package from `PyPI
<http://pypi.python.org/pypi/antispoofing.utils>`_ and unpack it in your
working area. The installation of the toolkit itself uses `buildout
<http://www.buildout.org/>`_. You don't need to understand its inner workings
to use this package. Here is a recipe to get you started::
  
  $ python bootstrap.py 
  $ ./bin/buildout

These 2 commands should download and install all non-installed dependencies and
get you a fully operational test and development environment.

.. note::

  The python shell used in the first line of the previous command set
  determines the python interpreter that will be used for all scripts developed
  inside this package. Because this package makes use of `Bob
  <http://idiap.github.com/bob>`_, you must make sure that the ``bootstrap.py``
  script is called with the **same** interpreter used to build Bob, or
  unexpected problems might occur.

  If Bob is installed by the administrator of your system, it is safe to
  consider it uses the default python interpreter. In this case, the above 3
  command lines should work as expected. If you have Bob installed somewhere
  else on a private directory, edit the file ``buildout.cfg`` **before**
  running ``./bin/buildout``. Find the section named ``buildout`` and edit the 
  line prefixes to point to the directory where Bob is installed or built. For
  example::

    [buildout]
    ...
    prefixes=/Users/crazyfox/work/bob/build


Problems
--------

In case of problems, please contact tiagofrepereira@gmail.com or ivana.chingovska@idiap.ch.


