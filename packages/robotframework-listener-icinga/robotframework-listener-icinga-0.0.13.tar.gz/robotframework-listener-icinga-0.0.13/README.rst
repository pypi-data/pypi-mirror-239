========
Overview
========

A Robot Framework listener for reporting via Icinga2 API.

* Free software: Apache Software License 2.0

Installation
============

::

    pip install robotframework-listener-icinga

You can also install the in-development version with::

    pip install https://gitlab.com/dominik.riva/robotframework-listener-icinga/-/archive/main/robotframework-listener-icinga-main.zip


Documentation
=============


To use the project:

.. code-block:: python

    import icinga
    icinga.longest()


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
