.. loop_wrapper documentation master file, created by
   sphinx-quickstart on Sat Jun 24 00:11:06 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to loop_wrapper's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

----------------------
The Basics
----------------------
``loop_wrapper`` is a job-control tool to make it easier to loop through datetime ranges.
``loop_wrapper`` can be instructed to loop through a range of dates and spawn a command you specify
for each date in the range. The command can be an excutable or a shell command.

Here is a first basic example: ::

        [$] loop_wrapper --quiet 19900101 19900105 echo "here is a date {d:%Y/%m/%d}"
        here is a date 1990/01/01
        here is a date 1990/01/02
        here is a date 1990/01/03
        here is a date 1990/01/04
        here is a date 1990/01/05

The ``loop_wrapper`` command-line has always such structure. ::

        [$] loop_wrapper [optional flags] <START-DATE> <STOP-DATE> <COMMAND>

In the first basic example above, ``--quiet`` is a flag that reduces verbosity. ``<START-DATE>`` is 01/01/1990,
``STOP-DATE`` is 5 days later 05/01/1990, and the ``<COMMAND>`` is a Bash ``echo`` invocation. The most important
part of this command is the ``{d:%Y/%m/%d}`` construct. This ``{d:}`` directive tells ``loop_wrapper`` how
to print the datetime at each date in the range. There must be at least one such ``{d:}`` construct in ``<COMMAND>``.

For the second example, consider you have an executable ``process`` (script or compiled it does not matter). Among other
parameters, ``process`` can take ``-d DDMMYYYY`` and will then do some processing for that day. Let's further assume
that ``process`` also takes a ``-i`` (input) ::

        [$] loop_wrapper 20150227 20150302 process -i /path/to/inputdir -d {d:%Y%m%d}
        CMD is process -i /path/to/inputdir -d {d:%Y%m%d}
        Serial run process -i /path/to/inputdir -d {d:%Y%m%d} from 2015-02-27 00:00:00 to 2015-03-02 00:00:00
        do  (process -i /path/to/inputdir -d 20150227)
        do  (process -i /path/to/inputdir -d 20150228)
        do  (process -i /path/to/inputdir -d 20150301)
        do  (process -i /path/to/inputdir -d 20150302)
        Done

Since we did not specify ``--quiet``, we get to see more information from ``loop_wrapper``,
including what ``COMMAND`` (``CMD``) is (1st line), that a *serial* run is prepared from 27/02/2015 to 02/03/2015 (2nd line),
the commands that the shell is instructed to run in turn (the *do (...)* lines). And finally that we are *Done*.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
