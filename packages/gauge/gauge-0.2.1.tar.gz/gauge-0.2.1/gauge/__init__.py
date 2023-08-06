# -*- coding: utf-8 -*-
"""
    gauge
    ~~~~~

    Deterministic linear gauge library.

    :copyright: (c) 2013-2014 by What! Studio
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import
from bisect import bisect_left
from collections import namedtuple
import weakref

from six.moves import map, zip
from sortedcontainers import SortedList, SortedListWithKey

from .common import ADD, REMOVE, TIME, VALUE, inf, now_or
from .deterministic import Determination, Segment


__all__ = ['Gauge', 'Momentum', 'inf', 'now_or']
__version__ = '0.2.1'


class Gauge(object):
    """Represents a gauge.  A gauge has a value at any moment.  It can be
    modified by an user's adjustment or an effective momentum.
    """

    #: The base time and value.
    base = (None, 0)

    #: A sorted list of momenta.  The items are :class:`Momentum` objects.
    momenta = None

    def __init__(self, value, max, min=0, at=None):
        at = now_or(at)
        self.base = (at, value)
        self.momenta = SortedListWithKey(key=lambda m: m[2])  # sort by until
        self._set_limits(max_=max, min_=min, at=at, forget_past=False)
        self._events = SortedList()
        self._links = set()

    @property
    def determination(self):
        """The cached determination.  If there's no the cache, it redetermines
        and caches that.

        A determination is a sorted list of 2-dimensional points which take
        times as x-values, gauge values as y-values.
        """
        try:
            return self._determination
        except AttributeError:
            pass
        # redetermine and cache.
        self._determination = Determination(self)
        return self._determination

    def invalidate(self):
        """Invalidates the cached determination.  If you touches the
        determination at the next first time, that will be redetermined.

        You don't need to call this method because all mutating methods such as
        :meth:`incr` or :meth:`add_momentum` calls it.
        """
        # invalidate linked gauges together.  A linked gauge refers this gauge
        # as a limit.
        for gauge in self.linked_gauges():
            gauge.invalidate()
        # remove the cached determination.
        try:
            del self._determination
        except AttributeError:
            pass

    def linked_gauges(self):
        """Yields linked gauges.  It removes dead links during an iteration."""
        try:
            links = list(self._links)
        except AttributeError:
            pass
        else:
            for gauge_ref in links:
                gauge = gauge_ref()
                if gauge is None:
                    self._links.remove(gauge_ref)
                    continue
                yield gauge

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, max):
        self.set_max(max)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, min):
        self.set_min(min)

    def get_max(self, at=None):
        """Predicts the current maximum value."""
        return self._max.get(at) if self._is_max_gauge else self._max

    def get_min(self, at=None):
        """Predicts the current minimum value."""
        return self._min.get(at) if self._is_min_gauge else self._min

    def _set_limits(self, max_=None, min_=None, clamp=False, at=None,
                    forget_past=True):
        limit_attrs = [x for x in [
            (max_, '_max', '_is_max_gauge'),
            (min_, '_min', '_is_min_gauge'),
        ] if x[0] is not None]
        at = now_or(at)
        forget_until = at
        flags = []
        for limit, attr, flag_attr in limit_attrs:
            try:
                prev_limit = getattr(self, attr)
            except AttributeError:
                prev_limit = None
            else:
                if getattr(self, flag_attr):
                    # unlink this gauge from the previous limiting gauge.
                    prev_limit._links.discard(weakref.ref(self))
            is_gauge = isinstance(limit, Gauge)
            flags.append(is_gauge)
            if is_gauge:
                # link this gauge to the new limiting gauge.
                limit._links.add(weakref.ref(self))
                forget_until = min(forget_until, limit.base[TIME])
        if forget_past:
            value = self.get(at=forget_until)
        for (limit, attr, flag_attr), flag in zip(limit_attrs, flags):
            # set the internal attribute.
            setattr(self, attr, limit)
            setattr(self, flag_attr, flag)
        self.invalidate()
        if clamp:
            value = self.clamp(value, at=at)
            forget_until = at
        if forget_past:
            self.forget_past(value, at=forget_until)

    def set_max(self, max, clamp=False, at=None):
        """Changes the maximum.

        :param max: a number or gauge to set as the maximum.
        :param clamp: limits the current value to be below the new maximum.
                      (default: ``True``)
        :param at: the time to change.  (default: now)
        """
        self._set_limits(max_=max, clamp=clamp, at=at)

    def set_min(self, min, clamp=False, at=None):
        """Changes the minimum.

        :param min: a number or gauge to set as the minimum.
        :param clamp: limits the current value to be above the new minimum.
                      (default: ``True``)
        :param at: the time to change.  (default: now)
        """
        self._set_limits(min_=min, clamp=clamp, at=at)

    def clamp(self, value, at=None):
        """Clamps by the limits at the given time.

        :param value: the value to clamp.
        :param at: the time to get limits.  (default: now)
        """
        at = now_or(at)
        max_ = self.get_max(at)
        if value > max_:
            return max_
        min_ = self.get_min(at)
        if value < min_:
            return min_
        return value

    def _predict(self, at=None):
        at = now_or(at)
        determination = self.determination
        if len(determination) == 1:
            # skip bisect_left() because it is expensive
            x = 0
        else:
            x = bisect_left(determination, (at,))
        if x == 0:
            return (determination[0][VALUE], 0.)
        try:
            time2, value2 = determination[x]
        except IndexError:
            return (determination[-1][VALUE], 0.)
        time1, value1 = determination[x - 1]
        value = Segment._calc_value(at, time1, time2, value1, value2)
        velocity = Segment._calc_velocity(time1, time2, value1, value2)
        if determination.inside_since is None:
            pass
        elif determination.inside_since <= time1:
            value = self.clamp(value, at=at)
        return (value, velocity)

    def get(self, at=None):
        """Predicts the current value.

        :param at: the time to observe.  (default: now)
        """
        value, velocity = self._predict(at)
        return value

    def velocity(self, at=None):
        """Predicts the current velocity.

        :param at: the time to observe.  (default: now)
        """
        value, velocity = self._predict(at)
        return velocity

    def goal(self):
        """Predicts the final value."""
        return self.determination[-1][VALUE]

    def incr(self, delta, over=False, clamp=False, at=None):
        """Increases the value by the given delta immediately.  The
        determination would be changed.

        :param delta: the value to increase.
        :param over: allow out of the range.
        :param clamp: clamp the value in the range.
        :param at: the time to increase.  (default: now)

        :raises ValueError: the value is out of the range.
        """
        at = now_or(at)
        prev_value = self.get(at=at)
        value = prev_value + delta
        max_, min_ = self.get_max(at), self.get_min(at)
        if over:
            pass
        elif clamp:
            if delta > 0 and value > max_:
                value = max(prev_value, max_)
            elif delta < 0 and value < min_:
                value = min(prev_value, min_)
        else:
            if delta > 0 and value > max_:
                raise ValueError('The value to set is bigger than the '
                                 'maximum ({0} > {1})'.format(value, max_))
            elif delta < 0 and value < min_:
                raise ValueError('The value to set is smaller than the '
                                 'minimum ({0} < {1})'.format(value, min_))
        self.forget_past(value, at=at)
        return value

    def decr(self, delta, over=False, clamp=False, at=None):
        """Decreases the value by the given delta immediately.  The
        determination would be changed.

        :param delta: the value to decrease.
        :param over: allow out of the range.
        :param clamp: clamp the value in the range.
        :param at: the time to decrease.  (default: now)

        :raises ValueError: the value is out of the range.
        """
        return self.incr(-delta, over=over, clamp=clamp, at=at)

    def set(self, value, over=False, clamp=False, at=None):
        """Sets the current value immediately.  The determination would be
        changed.

        :param value: the value to set.
        :param over: allow out of the range.
        :param clamp: clamp the value in the range.
        :param at: the time to set.  (default: now)

        :raises ValueError: the value is out of the range.
        """
        at = now_or(at)
        if clamp and not over:
            value = self.clamp(value, at=at)
        delta = value - self.get(at=at)
        return self.incr(delta, over=over, clamp=clamp, at=at)

    def when(self, value, after=0):
        """When the gauge reaches to the goal value.

        :param value: the goal value.
        :param after: take (n+1)th time.  (default: 0)

        :raises ValueError: the gauge will not reach to the goal value.
        """
        x = 0
        for x, at in enumerate(self.whenever(value)):
            if x == after:
                return at
        form = 'The gauge will not reach to {0}' + \
               (' more than {1} times' if x else '')
        raise ValueError(form.format(value, x))

    def whenever(self, value):
        """Yields multiple times when the gauge reaches to the goal value.

        :param value: the goal value.
        """
        if self.determination:
            determination = self.determination
            first_time, first_value = determination[0]
            if first_value == value:
                yield first_time
            zipped_determination = zip(determination[:-1], determination[1:])
            for (time1, value1), (time2, value2) in zipped_determination:
                if not (value1 < value <= value2 or value1 > value >= value2):
                    continue
                ratio = (value - value1) / float(value2 - value1)
                yield (time1 + (time2 - time1) * ratio)

    def _make_momentum(self, velocity_or_momentum, since=None, until=None):
        """Makes a :class:`Momentum` object by the given arguments.

        Override this if you want to use your own momentum class.

        :param velocity_or_momentum: a :class:`Momentum` object or just a
                                     number for the velocity.
        :param since: if the first argument is a velocity, it is the time to
                      start to affect the momentum.  (default: ``-inf``)
        :param until: if the first argument is a velocity, it is the time to
                      finish to affect the momentum.  (default: ``+inf``)

        :raises ValueError: `since` later than or same with `until`.
        :raises TypeError: the first argument is a momentum, but other
                           arguments passed.
        """
        if isinstance(velocity_or_momentum, Momentum):
            if not (since is until is None):
                raise TypeError('Arguments behind the first argument as a '
                                'momentum should be None')
            momentum = velocity_or_momentum
        else:
            velocity = velocity_or_momentum
            if since is None:
                since = -inf
            if until is None:
                until = +inf
            momentum = Momentum(velocity, since, until)
        since, until = momentum.since, momentum.until
        if since == -inf or until == +inf or since < until:
            pass
        else:
            raise ValueError('\'since\' should be earlier than \'until\'')
        return momentum

    def add_momentum(self, *args, **kwargs):
        """Adds a momentum.  A momentum includes the velocity and the times to
        start to affect and to stop to affect.  The determination would be
        changed.

        All arguments will be passed to :meth:`_make_momentum`.

        :returns: a momentum object.  Use this to remove the momentum by
                  :meth:`remove_momentum`.

        :raises ValueError: `since` later than or same with `until`.
        """
        momentum = self._make_momentum(*args, **kwargs)
        since, until = momentum.since, momentum.until
        self.momenta.add(momentum)
        self._events.add((since, ADD, momentum))
        if until != +inf:
            self._events.add((until, REMOVE, momentum))
        self.invalidate()
        return momentum

    def remove_momentum(self, *args, **kwargs):
        """Removes the given momentum.  The determination would be changed.

        All arguments will be passed to :meth:`_make_momentum`.

        :raises ValueError: the given momentum not in the gauge.
        """
        momentum = self._make_momentum(*args, **kwargs)
        try:
            self.momenta.remove(momentum)
        except ValueError:
            raise ValueError('{0} not in the gauge'.format(momentum))
        self.invalidate()

    def momentum_events(self):
        """Yields momentum adding and removing events.  An event is a tuple of
        ``(time, ADD|REMOVE, momentum)``.
        """
        yield (self.base[TIME], None, None)
        for time, method, momentum in list(self._events):
            if momentum not in self.momenta:
                self._events.remove((time, method, momentum))
                continue
            yield time, method, momentum
        yield (+inf, None, None)

    def _rebase(self, value=None, at=None, remove_momenta_before=None):
        """Sets the base and removes momenta between indexes of ``start`` and
        ``stop``.

        :param value: the value to set coercively.  (default: the current
                      value)
        :param at: the time to set.  (default: now)
        :param remove_momenta_before: the stopping index of momentum removal.
                                      (default: the last)
        """
        at = now_or(at)
        if value is None:
            value = self.get(at=at)
        self.base = (at, value)
        del self.momenta[:remove_momenta_before]
        self.invalidate()
        return value

    def clear_momenta(self, value=None, at=None):
        """Removes all momenta.  The value is set as the current value.  The
        determination would be changed.

        :param value: the value to set coercively.
        :param at: the time base.  (default: now)
        """
        return self._rebase(value, at=at)

    def forget_past(self, value=None, at=None):
        """Discards the momenta which doesn't effect anymore.

        :param value: the value to set coercively.
        :param at: the time base.  (default: now)
        """
        at = now_or(at)
        for gauge in self.linked_gauges():
            if gauge.base[TIME] < at:
                gauge.forget_past(at=at)
        x = self.momenta.bisect_left((-inf, -inf, at))
        value = self._rebase(value, at=at, remove_momenta_before=x)
        return value

    def __getstate__(self):
        limits = (self._max, self._min)
        momenta = list(map(tuple, self.momenta))
        return (self.base, limits, momenta)

    def __setstate__(self, state):
        base, limits, momenta = state
        max_, min_ = limits
        self.__init__(base[VALUE], max=max_, min=min_, at=base[TIME])
        for momentum in momenta:
            self.add_momentum(*momentum)

    def __repr__(self, at=None):
        """Example strings:

        - ``<Gauge 0.00/2.00>``
        - ``<Gauge 0.00 between 1.00~2.00>``
        - ``<Gauge 0.00 between <Gauge 0.00/2.00>~<Gauge 2.00/2.00>>``

        """
        at = now_or(at)
        value = self.get(at=at)
        hyper = False
        limit_reprs = []
        for limit in [self.max, self.min]:
            if isinstance(limit, Gauge):
                hyper = True
                limit_reprs.append('{0!r}'.format(limit))
            else:
                limit_reprs.append('{0:.2f}'.format(limit))
        form = '<{0} {1:.2f}'
        if not hyper and self.min == 0:
            form += '/{2}>'
        else:
            form += ' between {3}~{2}>'
        return form.format(type(self).__name__, value, *limit_reprs)


class Momentum(namedtuple('Momentum', ['velocity', 'since', 'until'])):
    """A power of which increases or decreases the gauge continually between a
    specific period.
    """

    def __new__(cls, velocity, since=-inf, until=+inf):
        velocity = float(velocity)
        return super(Momentum, cls).__new__(cls, velocity, since, until)

    def __repr__(self):
        string = '<{0} {1:+.2f}/s'.format(type(self).__name__, self.velocity)
        if self.since != -inf or self.until != +inf:
            string += ' ' + '~'.join([
                '' if self.since == -inf else '{0:.2f}'.format(self.since),
                '' if self.until == +inf else '{0:.2f}'.format(self.until)])
        string += '>'
        return string
