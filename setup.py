from distutils.core import setup

setup(
    name='mem_top',
    version='0.1.6',
    description='Shows top suspects for memory leaks in your Python program.',
    long_description='''
Usage::

    pip install mem_top
    from mem_top import mem_top

    # From time to time:
    logging.debug(mem_top()) # Or just print().

Result::

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

Explaining result:

* Noticed a leak of 6GB RAM and counting.
* Added "mem_top" and let it run for a while.
* When got the result above it became absolutely clear who is leaking here - the Python client of Gearman.
* Found its known bug - https://github.com/Yelp/python-gearman/issues/10
  leaking defaultdict of deques, and a dict of GearmanJobRequest-s,
  just as the "mem_top" showed.
* Replaced "python-gearman" - long story: stale 2.0.2 at PyPI, broken 2.0.X at github, etc.
* "mem_top" confirmed the leak is now completely closed.

UPDATES:

* Pass e.g. ``verbose_types=[dict, list]`` to get values sorted by repr length.
* Added "bytes" top.

SEE ALSO:

* https://docs.python.org/2/library/gc.html#gc.garbage
* https://pypi.python.org/pypi/objgraph

Config defaults::

    mem_top(
        limit=10, width=100, sep='\\n',
        refs_format='{num}\\t{type} {obj}', bytes_format='{num}\\t {obj}', types_format='{num}\\t {obj}',
        verbose_types=None, verbose_file_name='/tmp/mem_top',
    )
''',
    url='https://github.com/denis-ryzhkov/mem_top',
    author='Denis Ryzhkov',
    author_email='denisr@denisr.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    py_modules=['mem_top'],
)
