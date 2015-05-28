
This README file is for the loop_wrapper tool, that was designed to
help iterate commands over a range of dates, and parallelize the runs.

Typical usage:

Will "do something usefull" at all dates, using all available cpus:

[$] loop_wrapper --cpu all 20150101 20150315 do_something_usefull {d:%Y%m%d}
do_something_usefull 20150101
do_something_usefull 20150102
 ....
do_something_usefull 20150315

For full documentation, see:

loop_wrapper -h

For questions, bug reports and feature requests:

https://github.com/metno/loop_wrapper

loop_wrapper is maintained by T. Lavergne (t.lavergne@met.no) at the Norwegian Meteorological
Institute since 2013.

Licensed under GPLv2

