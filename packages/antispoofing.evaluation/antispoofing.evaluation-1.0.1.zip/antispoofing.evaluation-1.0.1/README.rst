==================================================================
Evaluation methods for verification systems under spoofing attacks
==================================================================

This package provides methods for evaluation of biometric verification systems under spoofing attacks. The evaluation is based on the Expected Performance and Spoofability Curve (EPSC). Using this package, you can compute thresholds based on EPSC, compute various error rates and plot various curves related to EPSC. 

Besides providing methods for plotting EPSC within your own scripts, this package brings several scripts that you can use to evaluate your own verification system (fused with an anti-spoofing system or not) from several perspectives. For example, you can: 
  - evaluate the threshold of a classification system on the development set
  - apply the threshold on an evaluation or any other set to compute different error rates
  - plot score distributions
  - plot different performance curves (DET, EPC and EPSC)

Furthermore, you can generate hypothetical data and use them to exemplify the above mentioned functionalities.

.. Finally, several scripts enable you to compare 4 state-of-the-art face verification systems, before and after they are fused with an anti-spoofing system for better robustness to spoofing. These systems are the ones that we use in our paper (to be announces soon), and have the following shortcuts: GMM, LBGPHS, GJet, and ISV, fused with different anti-spoofing systems using various fusion techniques. The scripts enable you to plot the relevant curves of the systems together and compare them.

If you use this package and/or its results, please cite the following
publication:

1. Our original paper on biometric evaluation (title, pdf and bibtex to be announced soon)::
 
    @ARTICLE{Chingovska_IEEETIFS_2014,
       author = {Chingovska, Ivana and Anjos, Andr{\'{e}} and Marcel, S{\'{e}}bastien},
       title = {Biometrics Evaluation Under Spoofing Attacks},
       journal = {IEEE Transactions on Information Forensics and Security},
       year = {2014},
    }
 
2. Bob_ as the core framework used to run the experiments::

    @inproceedings{Anjos_ACMMM_2012,
        author = {A. Anjos AND L. El Shafey AND R. Wallace AND M. G\"unther AND C. McCool AND S. Marcel},
        title = {Bob: a free signal processing and machine learning toolbox for researchers},
        year = {2012},
        month = oct,
        booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
        publisher = {ACM Press},
    }

If you wish to report problems or improvements concerning this code, please
contact the authors of the above mentioned papers.

Installation
------------

This package is a satellite package of Bob_
You will need a copy of it to run the algoritms.
Please download Bob_ from its webpage.

There are 2 options you can follow to get this package installed and
operational on your computer: you can use automatic installers like `pip
<http://pypi.python.org/pypi/pip/>`_ (or `easy_install
<http://pypi.python.org/pypi/setuptools>`_) or manually download, unpack and
use `zc.buildout <http://pypi.python.org/pypi/zc.buildout>`_ to create a
virtual work environment just for this package.

Using an automatic installer
============================

Using ``pip`` is the easiest (shell commands are marked with a ``$`` signal)::

  $ pip install antispoofing.evaluation

You can also do the same with ``easy_install``::

  $ easy_install antispoofing.evaluation

This will download and install this package plus any other required
dependencies. It will also verify if the version of Bob_ you have installed
is compatible.

This scheme works well with virtual environments by `virtualenv
<http://pypi.python.org/pypi/virtualenv>`_ or if you have root access to your
machine. Otherwise, we recommend you use the next option.

Using ``zc.buildout``
=====================

Download the latest version of this package from `PyPI
<http://pypi.python.org/pypi/antispoofing.evaluation>`_ and unpack it in your
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
  inside this package. Because this package makes use of Bob_, you must make sure that the ``bootstrap.py``
  script is called with the **same** interpreter used to build Bob_, or
  unexpected problems might occur.

  If Bob_ is installed by the administrator of your system, it is safe to
  consider it uses the default python interpreter. In this case, the above 3
  command lines should work as expected. If you have Bob_ installed somewhere
  else on a private directory, edit the file ``buildout.cfg`` **before**
  running ``./bin/buildout``. Find the section named ``external`` and edit the
  line ``egg-directories`` to point to the ``lib`` directory of the Bob_
  installation you want to use. For example::

    [external]
    recipe = xbob.buildout:external
    egg-directories=/Users/crazyfox/work/bob/build/lib


Using the package
-----------------

After downloading, go to the console and type::

  $ python bootstrap.py
  $ ./bin/buildout
  $ ./bin/sphinx-build docs sphinx

Now, the full documentation of the package, including a User Guide, will be availabe in ``sphinx/index.html``.

Problems
--------

In case of problems, please contact ivana.chingovska@idiap.ch


.. _bob: http://www.idiap.ch/software/bob
.. _idiap: http://www.idiap.ch
