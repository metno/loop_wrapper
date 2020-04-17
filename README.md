
[![Build Status](https://travis-ci.org/metno/loop_wrapper.png?branch=master)](https://travis-ci.org/metno/loop_wrapper)
[![Coverage Status](https://coveralls.io/repos/github/metno/loop_wrapper/badge.svg?branch=master)](https://coveralls.io/github/metno/loop_wrapper?branch=master)

``loop_wrapper`` will help iterate commands and scripts over a range of dates, and parallelize the runs.

Typical usage:

The following will run ``my_script.py`` (could be .sh, .pl, .exe, etc...) at all specified dates, using 3 cpus on your machine:

        [$] loop_wrapper --cpu 3 20150101 20150315 script.py {d:}
        my_script.py 20150101
        my_script.py 20150102
        ....
        my_script.py 20150315

For full documentation, and more cool features, see:

   https://loop-wrapper.readthedocs.io/

and

   ``loop_wrapper -h``

For questions, bug reports and feature requests:

   https://github.com/metno/loop_wrapper

Maintained since 2013 by Thomas Lavergne (Norwegian Meteorological Institute).

Licensed under GPLv2

