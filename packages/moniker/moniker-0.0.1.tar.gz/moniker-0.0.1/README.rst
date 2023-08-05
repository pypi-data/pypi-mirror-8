Moniker
=======

A simple batch file rename tool.

||Build Status|| |target|

Installation
============

Moniker is a simple Python utility for renaming and manipulating the
filesystem based off similar project and work from `Irving
Ruan <https://github.com/irvingruan/Moniker.git>`__.

Currently work in progress
--------------------------

Clone the repository

.. code:: bash

        $ git clone https://github.com/jjangsangy/moniker.git

Install

.. code:: bash

        $ python setup.py install

Usage
=====

.. code:: sh

        $ moniker . .py .python

.. code:: javascript

    {
        ".": [
            {
                "setup.py": "setup.python"
            }
        ], 
        "docs": [
            {
                "conf.py": "conf.python"
            }
        ], 
        "moniker": [
            {
                "__init__.py": "__init__.python"
            }, 
            {
                "__main__.py": "__main__.python"
            }, 
            {
                "__version__.py": "__version__.python"
            }, 
            {
                "moniker.py": "moniker.python"
            }
        ], 
        "moniker/tests": [
            {
                "__init__.py": "__init__.python"
            }, 
            {
                "test_main.py": "test_main.python"
            }
        ]
    }

.. ||Build Status|| image:: https://travis-ci.org/jjangsangy/Moniker
.. |Build Status| image:: https://travis-ci.org/jjangsangy/Moniker.svg?branch=master
.. |target| image:: https://badge.fury.io/py/py-translate.svg?branch=master
