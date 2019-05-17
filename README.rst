===============================
SciKit Data
===============================


.. image:: https://img.shields.io/pypi/v/scikit-data.svg
        :target: https://pypi.python.org/pypi/scikit-data

.. image:: https://img.shields.io/travis/OpenDataScienceLab/skdata.svg
        :target: https://travis-ci.org/OpenDataScienceLab/skdata

.. image:: https://readthedocs.org/projects/skdata/badge/?version=latest
        :target: https://skdata.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Conda package current release info
==================================

.. image:: https://anaconda.org/conda-forge/scikit-data/badges/version.svg
        :target: https://anaconda.org/conda-forge/scikit-data
        :alt: Anaconda-Server Badge

.. image:: https://anaconda.org/conda-forge/scikit-data/badges/downloads.svg
        :target: https://anaconda.org/conda-forge/scikit-data
        :alt: Anaconda-Server Badge


About SciKit Data
=================

The propose of this library is to allow the data analysis process more easy and automatic.

General objectives:

* reduce boilerplate code;
* reduce time spent on data analysis tasks and;
* offer a reproducible data analysis workflow.

Generally, there is a lot of boilerplate code on data analysis task that could be resolved with reproducible mechanisms and easy data visualization methods. Another point is related to data publish. A lot of data analysts doesn't know about open data repositories or doesn't consider that in his/her scientific workflow communication.

Specifics objectives:

* optimize data visualization;
* integration with open data repositories to publish data;
* reproducibility on data analysis tasks through storing and recovery operations;

SkData should integrate with Pandas library (Python).


Books used as reference to guide this project:
----------------------------------------------

- https://www.packtpub.com/big-data-and-business-intelligence/clean-data
- https://www.packtpub.com/big-data-and-business-intelligence/python-data-analysis
- https://www.packtpub.com/big-data-and-business-intelligence/mastering-machine-learning-scikit-learn
- https://www.packtpub.com/big-data-and-business-intelligence/practical-data-analysis-second-edition

Some other materials used as reference:
---------------------------------------

- https://github.com/rsouza/MMD/blob/master/notebooks/3.1_Kaggle_Titanic.ipynb
- https://github.com/agconti/kaggle-titanic/blob/master/Titanic.ipynb
- https://github.com/donnemartin/data-science-ipython-notebooks/blob/master/kaggle/titanic.ipynb


Installing scikit-data
======================

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


More Information
----------------

* License: MIT
* Documentation: https://skdata.readthedocs.io


References
----------

* CUESTA, Hector; KUMAR, Sampath. Practical Data Analysis. Packt Publishing Ltd, 2016.


**Electronic materials**

* [1] http://www.datasciencecentral.com/profiles/blogs/introduction-to-outlier-detection-methods
