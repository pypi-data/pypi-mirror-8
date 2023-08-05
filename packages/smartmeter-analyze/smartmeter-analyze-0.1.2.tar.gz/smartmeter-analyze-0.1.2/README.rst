======
README
======

This Tool was written to analyze your personal energy consumption.

The Tool currently only supports CSV files with daily consumption values, as
provided by the 'Smart Metering' service of 'Wiener Netze GmbH'.

Installation
============

::

    $ pip install smartmeter-analyze

Usage
=====

Print a statistical summary of your energy consumption::

    $ smutil summary consumption-file.csv

Print the summary, using multiple files or directories::

    $ smutil summary ~/some_dir_with_consumption_files/ another-file.csv

You can download your energy consumption data from smartmetering.wienernetze.at

Features
========

* Generation of basic consumption summaries (averages, peaks, etc.)
* Basic consumption prediction
* Handling of one or many (not necessarily disjunct) datasets

TODO
====

* More sophisticated summaries
* import/storage of data
* Report generation
* integration of pricing (energy only)

Credits
=======

Icon
----

The Icon was composed by the following pictograms:

* Graph designed by Pham Thi Dieu Linh from the thenounproject.com
* Socket designed by hunotika from the thenounproject.com
