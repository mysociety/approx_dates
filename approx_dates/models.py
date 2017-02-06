from __future__ import unicode_literals

import calendar
from datetime import date
import re

import six

class classproperty(object):
    """
    This decorator acts as @property (returning a new result
    from the method each time the property is requested) but
    for what would otherwise be a @classmethod.
    source: http://stackoverflow.com/a/13624858/223092
    """
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)



ISO8601_DATE_REGEX_YYYY_MM_DD = \
    re.compile(r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})$')
ISO8601_DATE_REGEX_YYYY_MM = \
    re.compile(r'^(?P<year>\d{4})-(?P<month>\d{2})$')
ISO8601_DATE_REGEX_YYYY = \
    re.compile(r'^(?P<year>\d{4})$')

_max_date = date(9999, 12, 31)
_min_date = date(1, 1, 1)


@six.python_2_unicode_compatible
class ApproxDate(object):

    @classproperty
    def FUTURE(cls):
        return cls(_max_date, _max_date)

    @classproperty
    def PAST(cls):
        return cls(_min_date, _min_date)

    def __init__(self, earliest_date, latest_date, source_string=None):
        self.earliest_date = earliest_date
        self.latest_date = latest_date
        self.source_string = source_string


    def is_partial_just_year(self):
        """
        Are our dates the start and end of a year?
        """
        ed = self.earliest_date
        ld = self.latest_date
        if ed.year == ld.year:
            if ed.month == 1 and ed.day == 1:
                return ld.month == 12 and ld.day == 31

    def is_partial_just_year_and_month(self):
        """
        Are the dates the start and end of a month?
        """
        ed = self.earliest_date
        ld = self.latest_date
        if ed.month == ld.month and ed.year == ld.year:
            days_in_month = calendar.monthrange(ed.year, ed.month)[1]
            return ed.day == 1 and ld.day == days_in_month

    def to_iso8601(self):
        """
        Convert the date range into the most compact
        iso8601 possible
        """
        if self.earliest_date == self.latest_date:
            return self.earliest_date.isoformat()
        else:
            if self.is_partial_just_year_and_month():
                return self.latest_date.strftime("%Y-%m")
            if self.is_partial_just_year():
                return "{0}".format(self.earliest_date.year)
        #if none of these - return a date range
        return "{0}/{1}".format(self.earliest_date.isoformat(),
                                self.latest_date.isoformat())

    @classmethod
    def from_iso8601(self, iso8601_date_string):
        if "/" in iso8601_date_string: #extract double date
            start,end = iso8601_date_string.split("/")
            start_date = ApproxDate.from_iso8601(start)
            end_date = ApproxDate.from_iso8601(end)
            combined = ApproxDate(start_date.earliest_date,
                                  end_date.latest_date,
                                  iso8601_date_string)
            return combined
        full_match = ISO8601_DATE_REGEX_YYYY_MM_DD.search(iso8601_date_string)
        if full_match:
            d = date(*(int(p, 10) for p in full_match.groups()))
            return ApproxDate(d, d, iso8601_date_string)
        no_day_match = ISO8601_DATE_REGEX_YYYY_MM.search(iso8601_date_string)
        if no_day_match:
            year = int(no_day_match.group('year'), 10)
            month = int(no_day_match.group('month'), 10)
            days_in_month = calendar.monthrange(year, month)[1]
            earliest = date(year, month, 1)
            latest = date(year, month, days_in_month)
            return ApproxDate(earliest, latest, iso8601_date_string)
        only_year_match = ISO8601_DATE_REGEX_YYYY.search(iso8601_date_string)
        if only_year_match:
            earliest = date(int(only_year_match.group('year'), 10), 1, 1)
            latest = date(int(only_year_match.group('year'), 10), 12, 31)
            return ApproxDate(earliest, latest, iso8601_date_string)
        msg = "Couldn't parse the ISO 8601 partial date '{0}'"
        raise ValueError(msg.format(iso8601_date_string))

    @property
    def midpoint_date(self):
        delta = self.latest_date - self.earliest_date
        return self.earliest_date + delta / 2

    @property
    def future(self):
        return self.earliest_date == _max_date and self.latest_date == _max_date

    @property
    def past(self):
        return self.earliest_date == _min_date and self.latest_date == _min_date

    def __str__(self):
        if self.source_string is not None:
            return six.text_type(self.source_string)
        if self.future:
            return 'future'
        if self.past:
            return 'past'
        return self.to_iso8601()

    def __eq__(self, other):
        if isinstance(other, date):
            return self.earliest_date == self.latest_date and \
               self.earliest_date == other
        if hasattr(other,"earliest_date") and hasattr(other,"latest_date"):
            return self.earliest_date == other.earliest_date and \
                self.latest_date == other.latest_date
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        if self.past:
            return six.text_type('ApproxDate.PAST')
        if self.future:
            return six.text_type('ApproxDate.FUTURE')
        if self.source_string:
            source_fmt = 'ApproxDate.from_iso8601({0})'
            return six.text_type(source_fmt.format(repr(self.source_string)))
        no_source_fmt =  'ApproxDate({0}, {1})'
        return six.text_type(no_source_fmt.format(
            repr(self.earliest_date), repr(self.latest_date)))

    @classmethod
    def possibly_between(cls, start_date, d, end_date):
        try:
            earlier_bound = start_date.earliest_date
        except AttributeError:
            earlier_bound = start_date
        try:
            later_bound = end_date.latest_date
        except AttributeError:
            later_bound = end_date
        return earlier_bound <= d <= later_bound
