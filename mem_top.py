"""
Shows top suspects for memory leaks in your Python program.

Usage:

    pip install mem_top
    from mem_top import mem_top

    # From time to time:
    logging.debug(mem_top()) # Or just print().

Please see full description here:
https://github.com/denis-ryzhkov/mem_top/blob/master/README.md

mem_top version 0.1.0  
Copyright (C) 2014 by Denis Ryzhkov <denisr@denisr.com>  
MIT License, see http://opensource.org/licenses/MIT
"""

#### import

from collections import defaultdict
import gc

#### mem_top

def mem_top(limit=10, width=100, sep='\n', refs_format='{num}\t{type} {obj}', types_format='{num}\t {obj}'):

    gc.collect()
    objs = gc.get_objects()

    nums_and_types = defaultdict(int)
    for obj in objs:
        nums_and_types[type(obj)] += 1

    return sep.join((
        '',
        'refs:',
        _top(limit, width, sep, refs_format, (
            (len(gc.get_referents(obj)), obj) for obj in objs
        )),
        '',
        'types:',
        _top(limit, width, sep, types_format, (
            (num, type) for type, num in nums_and_types.iteritems()
        )),
        '',
    ))

#### _top

def _top(limit, width, sep, format, nums_and_objs):
    return sep.join(
        format.format(num=num, type=type(obj), obj=repr(obj)[:width])
        for num, obj in sorted(nums_and_objs, key=lambda num_obj: -num_obj[0])[:limit]
    )

#### tests

if __name__ == '__main__':
    print(mem_top())
