# bprofile

A wrapper around profile/cProfile, gprof2dot and dot,
providing a simple context manager for profiling sections
of Python code and producing visual graphs of profiling results.

( 
[view on pypi](https://pypi.python.org/pypi/bprofile/);
[view on Bitbucket](https://bitbucket.org/cbillington/bprofile)
)

   * Install with `python setup.py install` 
   * Install the latest release version using `pip install bprofile` or `easy_install bprofile`
   * Requires Graphviz to be installed (gprof2dot is bundled)
   * Compatible with Windows and *nix
   
This package provides a single class:

    BProfile(output_path, threshold_percent=2.5, report_delay=5)
    
A profiling context manager. Outputs a .png graph made via profile/cProfile, gprof2dot
and graphviz. graphviz is the only external dependency.


### Example usage:

```
#!python
profile = BProfile('output.png')

with profile:
    do_some_stuff()

do_some_stuff_that_wont_be_profiled()

with profile:
    do_some_more_stuff()
```


### Arguments:

    - output_path:       the name of the .png file you would like to output. '.png'
                         will be appended if not present
                         
    - threshold_percent: int or float for the minimum percentage of total cumulative
                         time a call should have to be included in the output. 
                         Defaults to 2.5.
                         
    - report_delay:      How frequently output files should be produced. This is to
                         minimise overhead on your program, (even though this overhead
                         will only be incurred when no code is being profiled), while
                         allowing you to have somewhat immedaite results of the profiling
                         while your code is still running. Defaults to 5 (seconds).


### Output generation

The profiler will return immediately after the context manager, and will generate
its `.png` output after a delay (`report_delay`, default is 5 seconds) in a separate thread.
The delay is to allow the block to execute many times before report generation,
rather than slowing your program down with generating output all the time. This means
that if your profile block is running repeatedly, a new output file will be produced
every `report_delay` seconds.

Pending reports will be generated at interpreter shutdown if delay_time has not yet
elapsed.

Note that even if `report_delay` is short, it will not interfere with the profiling
results themselves, as a lock is acquired that will prevent profiled code from running
at the same time as the output generation code. So the overhead produced by output
generation does not affect the results of profiling - this overhead will only affect
portions of your code that are not being profiled.

The lock is shared between instances, and so you can freely instantiate many
Profile objects to profile different parts of your code (but give them different output
filenames!).
Profile objects are thread safe, so you can also pass the same Profile object to different
parts of your code to profile them on the same graph.

Note that since only one profiler can be running at a time, two profiled pieces of code
waiting on each other in any way will deadlock.