from __future__ import division
from collections import defaultdict
from decimal import Decimal

import gc
from itertools import groupby
import operator
import sys
import time
import timeit

import pytest

from .stats import RunningStats


def loadtimer(string):
    if '.' not in string:
        raise ValueError("Value for benchmark-timer must be in dotted form. Eg: 'module.attr'.")
    mod, attr = string.rsplit('.', 1)
    __import__(mod)
    mod = sys.modules[mod]
    return getattr(mod, attr)


def pytest_addoption(parser):
    group = parser.getgroup("benchmark")
    group.addoption(
        '--benchmark-max-time',
        action="store", type=Decimal, default=Decimal("0.5"),
        help="Maximum time to spend in a benchmark (including overhead)."
    )
    group.addoption(
        '--benchmark-max-iterations',
        action="store", type=int, default=5000,
        help="Maximum iterations to do."
    )
    group.addoption(
        '--benchmark-min-iterations',
        action="store", type=int, default=5,
        help="Minium iterations, even if total time would exceed `max-time`."
    )
    group.addoption(
        '--benchmark-timer',
        action="store", type=loadtimer, default=timeit.default_timer,
        help="Timer to use when measuring time."
    )
    group.addoption(
        '--benchmark-disable-gc',
        action="store_true", default=False,
        help="Disable GC during benchmarks."
    )
    group.addoption(
        '--benchmark-skip',
        action="store_true", default=False,
        help="Skip running any benchmarks."
    )
    group.addoption(
        '--benchmark-only',
        action="store_true", default=False,
        help="Only run benchmarks."
    )


class Benchmark(RunningStats):
    def __init__(self, name, disable_gc, timer, min_iterations, max_iterations, max_time, group=None):
        self._disable_gc = disable_gc
        self.name = name
        self.group = group
        self._timer = timer
        self._min_runs = min_iterations
        self._max_runs = max(max_iterations, max_iterations)
        # assert min_iterations <= max_iterations, (
        #    "Invalid configuration, min iterations need to be less than max "
        #    "iterations. You have %s min, %s max" % (min_iterations, max_iterations))
        self._max_time = max_time
        self._stats = RunningStats()
        self._called = False
        self._start = None
        self._gcenabled = None
        self._overall_start = None
        super(Benchmark, self).__init__()

    @property
    def done(self):
        if self._overall_start is None:
            self._overall_start = time.time()
        return not (
            self.runs < self._min_runs - 1 or
            (time.time() - self._overall_start) < self._max_time
        ) or self.runs >= self._max_runs - 1

    # TODO: implement benchmark function wrapper (that adds the timers), as alternative to context manager
    # def __call__(self, function):
    #     pass


    def __enter__(self):
        self._gcenabled = gc.isenabled()
        if self._disable_gc:
            gc.disable()
        self._start = self._timer()
        return self

    def __exit__(self, *exc):
        end = self._timer()
        if self._gcenabled:
            gc.enable()
        self.update(end - self._start)


class BenchmarkSession(object):
    def __init__(self, config):
        self._options = dict(
            max_time=config.getoption('benchmark_max_time'),
            max_iterations=config.getoption('benchmark_max_iterations'),
            min_iterations=config.getoption('benchmark_min_iterations'),
            timer=config.getoption('benchmark_timer'),
            disable_gc=config.getoption('benchmark_disable_gc'),
        )
        self._options['min_iterations'] = min(self._options['min_iterations'], self._options['max_iterations'])
        self._skip = config.getoption('benchmark_skip')
        self._only = config.getoption('benchmark_only')
        if self._skip and self._only:
            raise pytest.UsageError("Can't have both --benchmark-only and --benchmark-skip options.")
        self._benchmarks = []

    @pytest.fixture(scope="function")
    def benchmark(self, request):
        if self._skip:
            pytest.skip("Benchmarks are disabled.")
        else:
            node = request.node
            marker = node.get_marker('benchmark')
            options = marker.kwargs if marker else {}
            benchmark = Benchmark(node.name, **dict(self._options, **options))
            self._benchmarks.append(benchmark)
            return benchmark


    def pytest_runtest_call(self, item):
        benchmark = hasattr(item, 'funcargs') and item.funcargs.get('benchmark')
        if isinstance(benchmark, Benchmark):
            while not benchmark.done:
                item.runtest()
        else:
            if self._only:
                pytest.skip("Skipping non-benchmark (--benchmark-only active).")
            else:
                item.runtest()

    def pytest_terminal_summary(self, terminalreporter):
        tr = terminalreporter

        if not self._benchmarks:
            return

        groups = defaultdict(list)
        for bench in self._benchmarks:
            groups[bench.group].append(bench)
        for group, benchmarks in sorted(groups.items(), key=lambda pair: pair[0] or ''):
            tr.write_sep(
                '-',
                'benchmark{2}: {0} tests, {1.min_iterations} to {1.max_iterations} iterations,'
                ' {1.max_time:f}s max time'.format(
                    len(benchmarks),
                    type('', (), self._options),
                    "" if group is None else " %r" % group
                ),
                yellow=True
            )
            worst = {}
            best = {}
            for prop in ('min', 'max', 'avg', 'mean', 'stddev', 'runs'):
                worst[prop] = max(getattr(benchmark, prop) for benchmark in benchmarks)
            for prop in ('min', 'max', 'avg', 'mean', 'stddev'):
                best[prop] = min(getattr(benchmark, prop) for benchmark in benchmarks)
            widths = {
                'name': max(20, max(len(benchmark.name) for benchmark in benchmarks)),
                'runs': len(str(worst['runs'])),
            }

            overall_min = max(best.values())
            if overall_min < 0.000001:
                unit, adjustment = 'n', 1000000000
            if overall_min < 0.001:
                unit, adjustment = 'u', 1000000
            elif overall_min < 1:
                unit, adjustment = 'm', 1000
            else:
                unit, adjustment = '', 1

            for prop in ('min', 'max', 'avg', 'mean', 'stddev'):
                widths[prop] = min(6, max(
                    len("{0:.3f}".format(getattr(benchmark, prop) * adjustment))
                    for benchmark in benchmarks
                ))
            tr.write_line("{0:<{1}}   {2:>{3}}  {4:>{5}}  {6:>{7}}  {8:>{9}}  {10:>{11}}  {12:>{13}}".format(
                "Name (time in %ss)" % unit, widths['name'],
                'Min', widths['min'] + 3,
                'Max', widths['max'] + 3,
                'Avg', widths['avg'] + 3,
                'Mean', widths['mean'] + 3,
                'StdDev', widths['stddev'] + 3,
                'Iterations', widths['runs'] + 3,
            ))
            tr.write_line("-" * sum(widths.values(), 5 + len(widths) * 4))

            for benchmark in benchmarks:
                tr.write("{0:<{1}} ".format(benchmark.name, widths['name']))
                for prop in ('min', 'max', 'avg', 'mean', 'stddev'):
                    value = getattr(benchmark, prop)
                    tr.write(
                        "  {0:>{1}.3f}".format(value * adjustment, widths[prop] + 3),
                        green=value == best[prop],
                        red=value == worst[prop],
                        bold=True,
                    )
                tr.write(
                    "  {0:>{1}}".format(benchmark.runs, widths['runs'] + 5),
                )
                tr.write('\n')

            tr.write_line("-" * sum(widths.values(), 5 + len(widths) * 4))
            tr.write_line("")


def pytest_runtest_setup(item):
    benchmark = item.get_marker('benchmark')
    if benchmark:
        if benchmark.args:
            raise ValueError("benchmark mark can't have positional arguments.")
        for name in benchmark.kwargs:
            if name not in ('max_time', 'min_iterations', 'max_iterations', 'timer', 'group', 'disable_gc'):
                raise ValueError("benchmark mark can't have %r keyword argument." % name)


def pytest_configure(config):
    config.addinivalue_line("markers", "benchmark: mark a test with custom benchmark settings.")
    config.pluginmanager.register(BenchmarkSession(config), 'pytest-benchmark')
