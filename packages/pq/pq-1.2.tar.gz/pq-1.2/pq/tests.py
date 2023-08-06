# -*- coding: utf-8 -*-

import os
import sys

from json import dumps
from itertools import chain
from time import time, sleep
from math import sqrt
from datetime import datetime
from contextlib import contextmanager
from unittest import TestCase, SkipTest
from logging import getLogger, StreamHandler, INFO
from threading import Event, Thread, current_thread

from psycopg2cffi.pool import ThreadedConnectionPool
from psycopg2cffi import ProgrammingError
from psycopg2cffi.extensions import cursor

# Set up logging such that we can quickly enable logging for a
# particular queue instance (via the `logging` flag).
getLogger('pq').setLevel(INFO)
getLogger('pq').addHandler(StreamHandler())


def mean(values):
    return sum(values) / float(len(values))


def stdev(values, c):
    n = len(values)
    ss = sum((x - c) ** 2 for x in values)
    ss -= sum((x - c) for x in values) ** 2 / n
    return sqrt(ss / (n - 1))


class LoggingCursor(cursor):
    logger = getLogger('sql')

    def execute(self, sql, args=None):
        self.logger.info(self.mogrify(sql, args))

        try:
            cursor.execute(self, sql, args)
        except Exception as exc:
            self.logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise


class BaseTestCase(TestCase):
    base_concurrency = 1

    @classmethod
    def setUpClass(cls):
        c = cls.base_concurrency * 4
        pool = cls.pool = ThreadedConnectionPool(
            c, c, "dbname=pq_test user=postgres",
        )
        from pq import PQ
        cls.pq = PQ(
            pool=pool, table="queue",
        )

        try:
            cls.pq.create()
        except ProgrammingError as exc:
            # We ignore a duplicate table error.
            if exc.pgcode != '42P07':
                raise

    @classmethod
    def tearDownClass(cls):
        cls.pq.close()

    def setUp(self):
        self.queues = []
        self.start = time()

    def tearDown(self):
        for queue in self.queues:
            queue.clear()

    def make_one(self, name):
        queue = self.pq[name]
        self.queues.append(queue)
        queue.clear()
        return queue


class QueueTest(BaseTestCase):
    base_concurrency = 4

    @contextmanager
    def assertExecutionTime(self, condition, start=None):
        yield
        seconds = time() - (start or self.start)
        self.assertTrue(condition(seconds), seconds)

    def test_put_and_get(self):
        queue = self.make_one("test")
        queue.put({'foo': 'bar'})
        self.assertEqual(queue.get().data, {'foo': 'bar'})

    def test_put_and_get_pickle(self):
        queue = self.make_one("test/pickle")
        dt = datetime.utcnow()
        queue.put({'time': dt, 'text': '…æøå!'})
        self.assertEqual(queue.get().data, {'time': dt, 'text': '…æøå!'})

    def test_put_expected_at(self):
        queue = self.make_one("test")
        queue.put(1, None, "1s")
        queue.put(2, None, "2s")
        queue.put(3, None, "3s")
        queue.put(4, None, "4s")
        queue.put(5, None, "5s")
        t = time()
        self.assertEqual(len(queue), 5)
        for i, task in enumerate(queue):
            if task is None:
                break

            self.assertEqual(i + 1, task.data)
            d = time() - t
            self.assertTrue(d < 1)

        # We expect five plus the empty.
        self.assertEqual(i, 5)

    def test_put_schedule_at_without_blocking(self):
        queue = self.make_one("test_schedule_at_non_blocking")
        queue.put({'baz': 'fob'}, "6s")

        def get(block=True): return queue.get(block, 5)

        self.assertEqual(queue.get(False, 5), None)

    def test_put_schedule_at(self):
        queue = self.make_one("test_schedule_at_blocking")
        queue.put({'bar': 'foo'})
        queue.put({'baz': 'fob'}, "6s")
        queue.put({'foo': 'bar'}, "2s")
        queue.put({'boo': 'baz'}, "4s")

        # We use a timeout of five seconds for this test.
        def get(block=True): return queue.get(block, 5)

        # First item is immediately available.
        self.assertEqual(get(False).data, {'bar': 'foo'})

        with self.assertExecutionTime(lambda seconds: 2 < seconds < 3):
            self.assertEqual(get().data, {'foo': 'bar'})

        with self.assertExecutionTime(lambda seconds: 4 < seconds < 5):
            self.assertEqual(get().data, {'boo': 'baz'})

        with self.assertExecutionTime(lambda seconds: 6 < seconds < 7):
            self.assertEqual(get().data, {'baz': 'fob'})

        # This ensures the timeout has been reset
        with self.assertExecutionTime(
                lambda seconds: queue.timeout < seconds < queue.timeout + 1,
                time(),
        ):
            self.assertEqual(get(), None)

    def test_get_and_set(self):
        queue = self.make_one("test")
        queue.put({'foo': 'bar'})
        task = queue.get()
        self.assertEqual(task.data, {'foo': 'bar'})
        task.data = {'foo': 'boo'}

        with queue._transaction() as cursor:
            cursor.execute(
                "SELECT data FROM %s WHERE id = %s",
                (queue.table, task.id)
            )
            data = cursor.fetchone()[0]

        self.assertEqual(task.data, data)
        self.assertIn('size=%d' % len(dumps(data)), repr(task))

    def test_get_not_empty(self):
        queue = self.make_one("test")
        queue.put({'foo': 'bar'})

        with self.assertExecutionTime(lambda seconds: 0 < seconds < 0.1):
            self.assertEqual(queue.get().data, {'foo': 'bar'})

    def test_get_empty_blocking_timeout(self):
        queue = self.make_one("test_blocking_timeout")

        with self.assertExecutionTime(lambda seconds: seconds > 2):
            self.assertEqual(queue.get(timeout=2), None)

    def test_get_empty_non_blocking_timeout(self):
        queue = self.make_one("test")

        with self.assertExecutionTime(lambda seconds: seconds > 0.1):
            self.assertEqual(queue.get(), None)

    def test_get_empty_thread_puts(self):
        queue = self.make_one("test")

        def target():
            sleep(0.2)
            queue.put({'foo': 'bar'})

        thread = Thread(target=target)
        thread.start()

        with self.assertExecutionTime(lambda seconds: seconds < 1):
            self.assertEqual(queue.get().data, {'foo': 'bar'})

        thread.join()

    def test_get_empty_thread_puts_after_timeout(self):
        queue = self.make_one("test")

        def target():
            sleep(1.2)
            queue.put({'foo': 'bar'})

        thread = Thread(target=target)
        thread.start()

        with self.assertExecutionTime(lambda seconds: seconds > 0.1):
            self.assertEqual(queue.get(), None)

        thread.join()

    def test_get_empty_non_blocking_thread_puts(self):
        queue = self.make_one("test")

        def target():
            sleep(0.1)
            queue.put({'foo': 'bar'})

        thread = Thread(target=target)
        thread.start()
        t = time()
        self.assertEqual(queue.get(False), None, time() - t)
        sleep(0.2)
        self.assertEqual(queue.get(False).data, {'foo': 'bar'})
        thread.join()

    def test_iter(self):
        queue = self.make_one("test")
        data = {'foo': 'bar'}
        queue.put(data)

        def target():
            for i in xrange(5):
                sleep(0.2)
                queue.put(data)

        thread = Thread(target=target)
        thread.start()

        dt = []
        iterator = enumerate(queue)
        try:
            while True:
                t = time()
                i, task = next(iterator)
                self.assertEqual(data, task.data, (i, time() - t))
                dt.append(time() - t)
                if i == 5:
                    break
        finally:
            thread.join()

        self.assertGreater(0.1, dt[0])
        self.assertGreater(dt[1], 0.1)

    def test_length(self):
        queue = self.make_one("test")
        self.assertEqual(len(queue), 0)
        queue.put({'foo': 'bar'})
        self.assertEqual(len(queue), 1)
        queue.put({'foo': 'bar'})
        self.assertEqual(len(queue), 2)
        queue.get()
        self.assertEqual(len(queue), 1)

    def test_benchmark(self, items=1000):
        if not os.environ.get("BENCHMARK"):
            raise SkipTest

        event = Event()
        queue = self.make_one("benchmark")

        iterations = 1000
        threads = []

        # Queue.put
        def put(iterations=iterations):
            threads.append(current_thread())
            event.wait()
            for i in xrange(iterations):
                queue.put({})

        for i in xrange(self.base_concurrency):
            Thread(target=put).start()

        while len(threads) < self.base_concurrency:
            sleep(0.01)

        t = time()
        event.set()

        while threads:
            threads.pop().join()

        elapsed = time() - t
        put_throughput = iterations * self.base_concurrency / elapsed
        event.clear()

        # Queue.get
        def get(iterations=iterations):
            threads.append(current_thread())
            event.wait()
            iterator = iter(queue)
            iterator.timeout = 0.1
            for item in iterator:
                if item is None:
                    break

        for i in xrange(self.base_concurrency):
            Thread(target=get).start()

        while len(threads) < self.base_concurrency:
            sleep(0.1)

        t = time()
        event.set()

        while threads:
            threads.pop().join()

        elapsed = time() - t
        get_throughput = iterations * self.base_concurrency / elapsed
        event.clear()

        p_times = {}

        # Queue.__iter__
        def producer():
            thread = current_thread()
            times = p_times[thread] = []
            active[0].append(thread)
            event.wait()
            i = 0
            while True:
                t = time()
                queue.put({})
                times.append(time() - t)
                i += 1
                if i > items / self.base_concurrency:
                    break

        c_times = {}

        def consumer(consumed):
            thread = current_thread()
            times = c_times[thread] = []
            active[1].append(thread)
            event.wait()
            iterator = iter(queue)
            iterator.timeout = 0.1

            while True:
                t = time()
                try:
                    item = next(iterator)
                except StopIteration:
                    break

                if item is None:
                    break

                times.append(time() - t)
                consumed.append(item)

        # Use a trial run to warm up JIT (when using PyPy).
        warmup = '__pypy__' in sys.builtin_module_names
        c = self.base_concurrency

        for x in xrange(1 + int(warmup)):
            cs = [[] for i in xrange(c * 2)]

            threads = (
                [Thread(target=producer) for i in xrange(c)],
                [Thread(target=consumer, args=(cs[i], )) for i in xrange(c)],
            )

            active = ([], [])

            for thread in chain(*threads):
                thread.start()

            while map(len, active) != map(len, threads):
                sleep(0.1)

            event.set()
            t = time()

            for thread in chain(*threads):
                thread.join()

            event.clear()

        elapsed = time() - t
        consumed = sum(map(len, cs))

        c_times = [1000000 * v for v in chain(*c_times.values())]
        p_times = [1000000 * v for v in chain(*p_times.values())]

        get_latency = mean(c_times)
        put_latency = mean(p_times)

        get_stdev = stdev(c_times, get_latency)
        put_stdev = stdev(p_times, put_latency)

        sys.stderr.write("complete.\n>>> stats: %s ... " % (
            "\n           ".join(
            "%s: %s" % item for item in (
                ("threads       ", c),
                ("consumed      ", consumed),
                ("remaining     ", len(queue)),
                ("throughput    ", "%d items/s" % (consumed / elapsed)),
                ("get           ", "%d items/s" % (get_throughput)),
                ("put           ", "%d items/s" % (put_throughput)),
                ("get (mean avg)", "%d μs/item" % (get_latency)),
                ("put (mean avg)", "%d μs/item" % (put_latency)),
                ("get (stdev)   ", "%d μs/item" % (get_stdev)),
                ("put (stdev)   ", "%d μs/item" % (put_stdev)),
            ))))

    def test_producer_consumer_threaded(self):
        queue = self.make_one("test")

        def producer():
            ident = current_thread().ident
            for i in xrange(100):
                queue.put((ident, i))

        consumed = []

        def consumer():
            while True:
                for d in queue:
                    if d is None:
                        return

                    consumed.append(tuple(d.data))

        c = self.base_concurrency
        producers = [Thread(target=producer) for i in xrange(c * 2)]
        consumers = [Thread(target=consumer) for i in xrange(c)]

        for t in producers:
            t.start()

        for t in consumers:
            t.start()

        for t in producers:
            t.join()

        for t in consumers:
            t.join()

        self.assertEqual(len(consumed), len(set(consumed)))

    def test_context_manager_put(self):
        queue = self.make_one("test")

        with queue:
            queue.put({'foo': 'bar'})

        task = queue.get()
        self.assertEqual(task.data, {'foo': 'bar'})

    def test_context_manager_get_and_set(self):
        queue = self.make_one("test")
        queue.put({'foo': 'bar'})

        with queue:
            task = queue.get()
            self.assertEqual(task.data, {'foo': 'bar'})
            task.data = {'foo': 'boo'}

        with queue as cursor:
            cursor.execute(
                "SELECT data FROM %s WHERE id = %s",
                (queue.table, task.id)
            )
            data = cursor.fetchone()[0]

        self.assertEqual(task.data, data)
        self.assertIn('size=%d' % len(dumps(data)), repr(task))

    def test_context_manager_exception(self):
        queue = self.make_one("test")

        def test():
            with queue:
                queue.put({'foo': 'bar'})
                raise ValueError()

        self.assertRaises(ValueError, test)
        self.assertEqual(queue.get(), None)
