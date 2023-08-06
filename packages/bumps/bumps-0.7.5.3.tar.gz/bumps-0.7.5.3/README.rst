==============================================
Bumps: data fitting and uncertainty estimation
==============================================

Bumps provides data fitting and Bayesian uncertainty modeling for inverse
problems.  It has a variety of optimization algorithms available for locating
the most like value for function parameters given data, and for exploring
the uncertainty around the minimum.

Installation is with the usual python installation command:

    python setup.py install

This installs the package for all users of the system.  To isolate
the package it is useful to install virtualenv and virtualenv-wrapper.

This allows you to say:

    mkvirtualenv --system-site-packages bumps
    python setup.py develop

Once the system is installed, you can verify that it is working with: 

    bumps doc/examples/peaks/model.py --chisq

Documentation is available at `readthedocs <http://bumps.readthedocs.org/en/latest>`_

Relaase notes
=============

v0.7.5.3 2014-11-12
-------------------

* use --time to stop after a given number of hours
* Levenberg-Marquardt: fix "must be 1-d or 2-d" bug
* improve curvefit interface

v0.7.5.2 2014-09-26
-------------------

* pull numdifftools dependency into the repository

v0.7.5.1 2014-09-25
-------------------

* improve the load_model interface

v0.7.5 2014-09-10
-----------------

* Pure python release
