.. highlight:: shell

============
Installation
============

Using conda
-----------

Installing `scikit-data` from the `conda-forge` channel can be achieved by adding `conda-forge` to your channels with:

.. code-block:: console

   $ conda config --add channels conda-forge


Once the `conda-forge` channel has been enabled, `scikit-data` can be installed with:

.. code-block:: console

   $ conda install scikit-data


It is possible to list all of the versions of `scikit-data` available on your platform with:

.. code-block:: console

   $ conda search scikit-data --channel conda-forge


Using pip
---------

To install scikit-data, run this command in your terminal:

.. code-block:: console

    $ pip install skdata

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for scikit-data can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/OpenDataScienceLab/skdata

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/OpenDataScienceLab/skdata/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/OpenDataScienceLab/skdata
.. _tarball: https://github.com/OpenDataScienceLab/skdata/tarball/master
