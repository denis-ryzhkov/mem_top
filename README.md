# mem_top

Shows top suspects for memory leaks in your Python program.

## Usage

    pip install mem_top
    from mem_top import mem_top

    # From time to time:
    logging.debug(mem_top())
    # print(mem_top())

    # Notice which counters keep increasing over time - they are the suspects.

## Counters

`mem_top` iterates all objects found in memory and calculates:

* refs - number of direct references from this object to other objects, like keys and values of dict
    * E.g. a dict `{("some", "complex", "key"): "value"}` will have `refs: 2` - 1 ref for key, 1 ref for value
    * Its key `("some", "complex", "key")` will have `refs: 3` - 1 ref per item
* bytes - size of this object in bytes
* types - number of objects of this type still kept in memory after garbage collection

## Real life example

    refs:
    144997  <type 'collections.defaultdict'> defaultdict(<type 'collections.deque'>, {<GearmanJobRequest task='...', unique='.
    144996  <type 'dict'> {'.:..............:.......': <GearmanJobRequest task='..................', unique='.................
    18948   <type 'dict'> {...
    1578    <type 'dict'> {...
    968     <type 'dict'> {...
    968     <type 'dict'> {...
    968     <type 'dict'> {...
    767     <type 'list'> [...
    726     <type 'dict'> {...
    608     <type 'dict'> {...

    types:
    292499  <type 'dict'>
    217912  <type 'collections.deque'>
    72702   <class 'gearman.job.GearmanJob'>
    72702   <class 'gearman.job.GearmanJobRequest'>
    12340   <type '...
    3103    <type '...
    1112    <type '...
    855     <type '...
    767     <type '...
    532     <type '...

* Noticed a leak of 6GB RAM and counting.
* Added "mem_top" and let it run for a while.
* When got the result above it became absolutely clear who is leaking here:  
the Python client of Gearman kept increasing its counters over time.
* Found its known bug - https://github.com/Yelp/python-gearman/issues/10  
leaking defaultdict of deques, and a dict of GearmanJobRequest-s,  
just as the "mem_top" showed.
* Replaced "python-gearman" - long story: stale 2.0.2 at PyPI, broken 2.0.X at github, etc.
* "mem_top" confirmed the leak is now completely closed.

## Updates

* Pass e.g. `verbose_types=[dict, list]` to store their values,
  sorted by `repr` length descending,
  in `verbose_file_name` or returned from `mem_top()`.
* Added "bytes" top.

## Config defaults

```
mem_top(
    limit=10,                           # limit of top lines per section
    width=100,                          # width of each line in chars
    sep='\n',                           # char to separate lines with
    refs_format='{num}\t{type} {obj}',  # format of line in "refs" section
    bytes_format='{num}\t {obj}',       # format of line in "bytes" section
    types_format='{num}\t {obj}',       # format of line in "types" section
    verbose_types=None,                 # list of types to sort values by `repr` length
    verbose_file_name='/tmp/mem_top',   # name of file to store verbose values in
)
```

## See also

* https://docs.python.org/2/library/gc.html#gc.garbage
* https://pypi.python.org/pypi/objgraph

## About

mem_top version 0.2.1  
Copyright (c) 2014-2022 Denis Ryzhkov <denisr@denisr.com>  
MIT License
