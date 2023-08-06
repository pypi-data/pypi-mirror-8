=======
pyJHTDB
=======

Python wrapper for the JHU Turbulence Database Cluster library.
More information can be found at http://turbulence.pha.jhu.edu/.

Installing pypi version
=======================

If you have ``pip``, you can simply do this::

    pip install pyJHTDB

If you're running unix (i.e. some MacOS or GNU/Linux variant), you will
probably need to have a ``sudo`` in front of the ``pip`` command.
If you don't have ``pip`` on your system, it is quite easy to get it
following the instructions at
http://pip.readthedocs.org/en/latest/installing.html.

Installing from source
======================

ubuntu 14.04
------------

Bare-bone installation::

    sudo apt-get install build-essential gfortran
    sudo apt-get install python-setuptools
    sudo apt-get install python-dev
    sudo easy_install numpy
    sudo python setup.py install

Note that doing this should, in principle, also install ``sympy`` on
your system, since it's used by ``pyJHTDB``.

Happy fun installation::

    sudo apt-get install build-essential gfortran
    sudo apt-get install python-setuptools
    sudo apt-get install python-dev
    sudo apt-get install libpng-dev libfreetype6-dev
    sudo apt-get install libhdf5-dev
    sudo easy_install numpy
    sudo easy_install h5py
    sudo easy_install matplotlib
    sudo python setup.py install

I haven't tested the installation on any other system, but I think
reasonable variations on the above should work for the minimal
installation on all unix systems (i.e. for MacOS as well).
If you manage to get it working (i.e. you import test_plain like the
README says and you can run it), please let me know what steps you
needed to take for your system, so I can append the instructions to
this file.

Basic usage
===========

Although this particular Python wrapper is still a work in progress, it
is mature enough to be used in production work.

On first contact with this library, we recommend that you first run
"test_plain". To be more specific:

.. code:: python

    from pyJHTDB import test_plain
    test_plain()

The code that is executed can be found in "pyJHTDB/test.py", and it's
the simplest example of how to access the turbulence database.

Configuration
-------------

While our service is open to anyone, we would like to keep track of who
is using the service, and how. To this end, we would like each user or
site to obtain an authorization token from us:
http://turbulence.pha.jhu.edu/help/authtoken.html
For simple experimentation, the default token included in the package
should be valid.

If you do obtain an authorization token, please write it in the file
``auth_token.txt``, in the folder ``.config/JHTDB`` from your home
folder. This folder should be generated automatically upon first
importing the package.

The ``.config/JHTDB`` folder is also used to store data used by the
``pyJHTDB.interpolator.spline_interpolator`` class, including shared
libraries. If you do not plan on using the local interpolation
functionality, no data files will be generated.

