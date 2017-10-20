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

    The data analysis process is composed of following steps:

    * The statement of problem
    * Collecting your data
    * Cleaning the data
    * Normalizing the data
    * Transforming the data
    * Exploratory statistics
    * Exploratory visualization
    * Predictive modeling
    * Validating your model
    * Visualizing and interpreting your results
    * Deploying your solution

    (Cuesta, Hector and Kumar, Sampath; 2016)

This project contemplates the follow features:

* Data Preparation
* Data Exploration
* Prepare data to Predictive modeling
* Visualizing results
* Reproducible data analysis


Data Preparation
----------------

    Data preparation is about how to obtain, clean, normalize, and transform the data into an
    optimal dataset, trying to avoid any possible data quality issues such as invalid, ambiguous,
    out-of-range, or missing values.

    (...)

    Scrubbing data, also called data cleansing, is the process of correcting or
    removing data in a dataset that is incorrect, inaccurate, incomplete,
    improperly formatted, or duplicated.

    (...)

    In order to avoid dirty data, our dataset should possess the following characteristics:

    * Correct
    * Completeness
    * Accuracy
    * Consistency
    * Uniformity

    (...)

    **Data transformation**

    Data transformation is usually related to databases and data warehouses where values from
    a source format are extract, transform, and load in a destination format.

    Extract, Transform, and Load (ETL) obtains data from various data sources, performs some
    transformation functions depending on our data model, and loads the resulting data into
    the destination.


    (Cuesta, Hector and Kumar, Sampath; 2016)

Data exploration
----------------

    Data exploration is essentially looking at the processed data in a graphical or statistical form
    and trying to find patterns, connections, and relations in the data. Visualization is used to
    provide overviews in which meaningful patterns may be found.

    (...)

    The goals of exploratory data analysis are as follows:

    * Detection of data errors
    * Checking of assumptions
    * Finding hidden patters (like tendency)
    * Preliminary selection of appropriate models
    * Determining relationships between the variables


    (Cuesta, Hector and Kumar, Sampath; 2016)


Prepare data to Predictive modeling
-----------------------------------

    From the galaxy of information we have to extract usable hidden patterns and trends using
    relevant algorithms. To extract the future behavior of these hidden patterns, we can use
    predictive modeling. Predictive modeling is a statistical technique to predict future
    behavior by analyzing existing information, that is, historical data. We have to use proper
    statistical models that best forecast the hidden patterns of the data or
    information (Cuesta, Hector and Kumar, Sampath; 2016).

SkData, should allow you to format your data to send it to some predictive library
as scikit-learn.


Visualizing results
-------------------

    In an explanatory data analysis process, simple visualization techniques are very useful for
    discovering patterns, since the human eye plays an important role. Sometimes, we have to
    generate a three-dimensional plot for finding the visual pattern. But, for getting better
    visual patterns, we can also use a scatter plot matrix, instead of a three-dimensional plot. In
    practice, the hypothesis of the study, dimensionality of the feature space, and data all play
    important roles in ensuring a good visualization technique (Cuesta, Hector and Kumar, Sampath; 2016).


Quantitative and Qualitative data analysis
------------------------------------------

    Quantitative data are numerical measurements expressed in terms of numbers.

    Qualitative data are categorical measurements expressed in terms of natural language
    descriptions.

    Quantitative analytics involves analysis of numerical data. The type of the analysis will
    depend on the level of measurement. There are four kinds of measurements:

    * Nominal data has no logical order and is used as classification data.
    * Ordinal data has a logical order and differences between values are not constant.
    * Interval data is continuous and depends on logical order. The data has standardized differences between values, but do not include zero.
    * Ratio data is continuous with logical order as well as regular intervals differences between values and may include zero.

    Qualitative analysis can explore the complexity and meaning of social phenomena. Data for
    qualitative study may include written texts (for example, documents or e-mail) and/or
    audible and visual data (digital images or sounds).

    (Cuesta, Hector and Kumar, Sampath; 2016)


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
