The APE (Read Me)
=================


The `All-Purpose Executor` is a plugin-based system meant to create a unified front-end for different device-related testing. 

Installation
------------

To install it you can use the ``setup.py`` file to install it.

.. code-block:: bash

   python setup.py install

If you are installing it system-wide you will probably have to prefix this and other install commands with ``sudo``.

Documentation
-------------

The APE has some online help.

.. code-block:: bash

   ape -h

::

    APE (the all-purpose-evaluator)
    
    Usage: ape -h | -v
           ape [--debug|--silent] [--pudb|--pdb] <command> [<argument>...]
           ape [--debug|--silent] [--trace|--callgraph] <command> [<argument>..
    .]
    
    Help Options:
    
        -h, --help     Display this help message and quit.
        -v, --version  Display the version number and quit.
        
    Logging Options:
    
        --debug   Set logging level to DEBUG.
        --silent  Set logging level to ERROR.
    
    Debugging Options:
    
        --pudb       Enable the `pudb` debugger (if installed)
        --pdb        Enable the `pdb` (python's default) debugger
        --trace      Enable code-tracing
        --callgraph  Create a call-graph of for the code
    
    Positional Arguments:
    
        <command>      The name of a sub-command (see below)
        <argument>...  One or more options or arguments for the sub-command
        
    Available Sub-Commands:
    
        run    Run a plugin
        fetch  Fetch a sample configuration-file
        help   Display more help
        list   List known plugins
        check  Check a configuration
    
    To get help for a sub-command pass `-h` as the argument. e.g.:
    
        ape run -h
    
    
    



Installing Testing Dependencies
-------------------------------

The APE is currently being tested using `behave <http://pythonhosted.org/behave/>`_ so if you want to run the tests, you'll need that, `pyhamcrest <http://pyhamcrest.readthedocs.org/en/1.8.0/>`_ and `mock <http://mock.readthedocs.org/en/latest/magicmock.html>`_. All three are on pypi so if you have pip installed you can install them from the web (if installing system wide run as root).

.. code-block:: bash

   pip install behave
   pip install pyhamcrest
   pip install mock

