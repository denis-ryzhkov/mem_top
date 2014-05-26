from distutils.core import setup

setup(
    name='mem_top',
    version='0.1.0',
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

* It is absolutely clear who is leaking here, it is Python client of Gearman.
* Found its known bug - leaking defaultdict of deques, and a dict of GearmanJobRequest-s: https://github.com/Yelp/python-gearman/issues/10
* Found this bug is already fixed, but PyPI at https://pypi.python.org/pypi/gearman still has an old broken code.
* Replaced "pip install gearman" with "pip install git+https://github.com/Yelp/python-gearman.git".
* Repeated "mem_top" test, and confirmed the leak is completely closed.

Config defaults::

    mem_top(limit=10, width=100, sep='\\n', refs_format='{num}\\t{type} {obj}', types_format='{num}\\t {obj}')

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
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    py_modules=['mem_top'],
)
