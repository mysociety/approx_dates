approx_dates: represent partial or approximate dates in Python
==============================================================

[This is a preliminary version of this library (hence the 0.*
version number) and the API may change.]

It's frequently useful to be able to represent partial or
approximate dates in Python.  Colloquially, examples of these
might be:

* 1963 (i.e. just the year, with no month or day specified)
* March 1979 (i.e. just the year and the month, with no day
  specified)
* At some point before the 21st of July 2015
* At some point after 1st January 2000
* Some point between 25th and 31st of December 2016
* At an arbitrary or unknown point in the past
* At an arbitrary or unknown point in the future

The ``ApproxDate`` class can represent all of the above, as well
as precise dates, where the exact year, month and day is known.

This package has been tested on Python 2.7 and Python 3.5.

Similar Packages
~~~~~~~~~~~~~~~~

The alternative to this package that I'm aware of is the
``ApproximateDate`` class from `django-date-extensions
<https://github.com/dracos/django-date-extensions>`__. This has
a different model for approximate dates - they can be ``past``,
``future``, ``YYYY``, ``YYYY-MM`` or ``YYYY-MM-DD``, whereas the
``ApproxDate`` model in this package can also represent a date
which is known to be between two arbitrary dates, or is known to
be before (or after) some particular date.

Installation
------------

You can install this package with:

.. code:: bash

   pip install approx_dates

Usage
-----

You can create a full date or a partial date from the an ISO
8601 string:

.. code:: python

   from approx_dates.models import ApproxDate

   ApproxDate.from_iso8601('1215-06-15')
   ApproxDate.from_iso8601('1215-06')
   ApproxDate.from_iso8601('1215')

Or you can reprent points arbitrarily far in the past or future
with:

.. code:: python

   ApproxDate.PAST
   ApproxDate.FUTURE

To represent a date that's somewhere within two bounds, you can
specify two endpoints. For example:

.. code:: python

   from datetime import date

   ApproxDate(date(2016, 12, 25), date(2016, 12, 31))

These endpoints are intended to be inclusive. For example, the
above ``ApproxDate`` might represent the 25th, 26th, ... or the
31st of December 2016.

You can test whether an ``ApproxDate`` represents arbitrarily
far in the future or in the past with the ``past`` and
``future`` properties which evaluate to ``True`` or ``False``.

To convert an ``ApproxDate`` into one of core Python's
``datetime.date`` objects, you can use on of the following
methods:

.. code:: python

   ad = ApproxDate.from_iso8601('1979-03')

   ad.earliest_date
   >>> datetime.date(1979, 3, 1)

   ad.latest_date
   >>> datetime.date(1979, 3, 31)

   ad.midpoint_date
   >>> datetime.date(1979, 3, 16)

Obviously, whether one ``ApproxDate`` is earlier or later than
another is ill-defined, so the ``__lt__``, ``__gt__``,
``__lte__`` and ``__gte__`` magic methods are not defined on
``ApproxDate``.  If you need to compare two ``ApproxDate``
objects, you need to first convert it to a ``datetime.date``
using one of the methods above.

The ``__eq__`` and ``__ne__`` magic methods are defined, so that
two approx dates can be tested for whether they represent
exactly the same possible range of dates.  If the right hand
side of an equality or inequality comparison is a
``datetime.date``, it will treated equal if the ``ApproxDate``
on the left is precise to a day, and reprents the same date.

You can also test whether a ``datetime.date`` might be between
two ``ApproxDate`` or ``datetime.date`` objects using the
``ApproxDate.possibly_between`` class method, e.g.:

.. code:: python

   d1 = ApproxDate.from_iso8601('2000')
   d2 = ApproxDate.from_iso8601('2005')
   ApproxDate.possibly_between(d1, date(2000, 7, 1), d2)
   >>> True

   ApproxDate.possibly_between(d1, date(1999, 12, 31), d2)
   >>> True

Development
-----------

After cloning this repository, you can install the dependencies
for development with:

.. code:: bash

   pip install -e .
   pip install tox

And then run the tests with:

.. code:: bash

   tox
