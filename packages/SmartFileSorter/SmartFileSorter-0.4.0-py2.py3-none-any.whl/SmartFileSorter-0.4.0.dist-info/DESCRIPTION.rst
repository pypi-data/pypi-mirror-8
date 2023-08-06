===============================
Smart File Sorter
===============================

.. image:: https://badge.fury.io/py/SmartFileSorter.png
    :target: http://badge.fury.io/py/SmartFileSorter

.. image:: https://travis-ci.org/jashort/SmartFileSorter.png?branch=master
        :target: https://travis-ci.org/jashort/SmartFileSorter

.. image:: https://pypip.in/download/SmartFileSorter/badge.png
        :target: https://pypi.python.org/pypi/SmartFileSorter


Rule based file moving and renaming tool

* Free software: BSD license
* Documentation: https://smartfilesorter.readthedocs.org.

Features
--------

* Moves/renames files based on rules defined in a YAML configuration file.
* Automatically renames a file if it already exists in the destination directory by appending a sequence number to the
  filename. (file.txt, file_001.txt, file_002.txt, etc)
* Easy to extend with new match or action rules




History
-------
0.4.0 (2014-11-18)
--------------------

* Fixed bug that threw an error when running under Python3

0.3.0 (2014-11-18)
--------------------

* Processing will stop for a file after the first ruleset matches and actions are performed.
* Added test for that
* Tests will clean up temporary files after they run
* Log files that match a rule at the debug level instead of info (less verbose output at standard log level)
* After running, log the number of files that each ruleset matched.


0.2.0 (2014-09-15)
---------------------

* Fixed badge link in README.rst
* Updated documentation with examples and added plugin description and usage examples


0.1.0 (2014-09-14)
---------------------

* First release on PyPI.

