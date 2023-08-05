#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  Copyright 2014 Adam Fiebig <fiebig.adam@gmail.com>
#  Originally based on "wishbone" project by smetj
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from uuid import uuid4
from collections import deque
from compysition.errors import QueueEmpty, QueueFull, ReservedName, QueueMissing
from gevent import sleep
from gevent.event import Event
from time import time


class Container():
    pass


class QueuePool(object):

    def __init__(self, size):
        self.__size = size
        self.queues = Container()
        self.queues.metrics = Queue("metrics", max_size=size)
        self.queues.logs = Queue("logs", max_size=size, fallthrough=False)
        self.queues.failed = Queue("failed", max_size=size)
        self.inbound_queues = Container()
        self.outbound_queues = Container()
        self.error_queues = Container()

    def listOutboundQueues(self, names=False, default=True):
        '''returns the list of queue names from the queuepool.
        '''

        if default:
            blacklist = []
        else:
            blacklist = ['failed', 'logs', 'metrics']

        for m in self.outbound_queues.__dict__.keys():
            if m not in blacklist:
                if not names:
                    yield getattr(self.outbound_queues, m)
                else:
                    yield m

    def listQueues(self, names=False, default=True):
        '''returns the list of queue names from the queuepool.
        '''

        if default:
            blacklist = []
        else:
            blacklist = ['failed', 'logs', 'metrics']

        for m in self.queues.__dict__.keys():
            if m not in blacklist:
                if not names:
                    yield getattr(self.queues, m)
                else:
                    yield m

    def listInboundQueues(self, names=False):
        '''returns the list of queue names from the queuepool.
        '''
        for m in self.inbound_queues.__dict__.keys():
            if not names:
                yield getattr(self.inbound_queues, m)
            else:
                yield m

    def listErrorQueues(self, names=False):
        for m in self.error_queues.__dict__.keys():
            if not names:
                yield getattr(self.error_queues, m)
            else:
                yield m

    def createErrorQueue(self, name):
        '''Creates an error Queue.'''
        if name in ["metrics", "logs", "failed"]:
            raise ReservedName

        queue = Queue(name, max_size=self.__size)
        setattr(self.queues, name, queue)
        setattr(self.error_queues, name, queue)

    def createInboundQueue(self, name):
        '''Creates an inbound Queue.'''
        if name in ["metrics", "logs", "failed"]:
            raise ReservedName

        queue = Queue(name, max_size=self.__size)
        setattr(self.queues, name, queue)
        setattr(self.inbound_queues, name, queue)

    def addOutboundQueue(self, queue, name=None):
        '''Adds an existing outbound Queue.'''


        if name is None:
            name = queue.name

        if queue.name in ["metrics", "logs", "failed"]:
            raise ReservedName



        setattr(self.queues, name, queue)
        setattr(self.outbound_queues, name, queue)

    def addInboundQueue(self, queue, name=None):
        '''Adds an existing outbound Queue.'''
        #if queue.name in ["metrics", "logs", "failed"]:
        #    raise ReservedName
        if name is None:
            name = queue.name

        setattr(self.queues, name, queue)
        setattr(self.inbound_queues, name, queue)

    def createOutboundQueue(self, name):
        '''Creates an outbound Queue.'''
        if name in ["metrics", "logs", "failed"]:
            raise ReservedName

        queue = Queue(name, max_size=self.__size)
        setattr(self.queues, queue.name, queue)
        setattr(self.outbound_queues, queue.name, queue)

    def hasQueue(self, name):
        '''Returns true when queue with <name> exists.'''

        try:
            getattr(self.queues, name)
            return True
        except:
            return False

    def getQueue(self, name):
        '''Convenience funtion which returns the queue instance.'''

        try:
            return getattr(self.queues, name)
        except:
            raise QueueMissing

    def join(self):
        '''Blocks until all queues in the pool are empty.'''
        for queue in self.listQueues():
            queue.waitUntilEmpty()
            # while True:
            #     if queue.size() > 0:
            #         sleep(0.1)
            #     else:
            #         break


class Queue(object):

    '''A queue used to organize communication messaging between Compysition Actors.

    Parameters:

        - max_size (int):   The max number of elements in the queue.
                            Default: 1

    When a queue is created, it will drop all messages. This is by design.
    When <disableFallThrough()> is called, the queue will keep submitted
    messages.  The motivation for this is that when is queue is not connected
    to any consumer it would just sit there filled and possibly blocking the
    chain.

    The <stats()> function will reveal whether any events have disappeared via
    this queue.

    '''

    def __init__(self, name, max_size=1, fallthrough=True, *args, **kwargs):
        self.max_size = max_size
        self.id = str(uuid4())
        self.name = name
        self.__q = deque()
        self.__in = 0
        self.__out = 0
        self.__dropped = 0
        self.__cache = {}

        self.__empty = Event()
        self.__empty.set()

        self.__free = Event()
        self.__free.set()

        self.__full = Event()
        self.__full.clear()

        self.__content = Event()
        self.__content.clear()

        if fallthrough:
            self.put = self.__fallThrough
        else:
            self.put = self.__put

    def clean(self):
        '''Deletes the content of the queue.
        '''
        self.__q = deque()

    def disableFallThrough(self):
        self.put = self.__put

    def dump(self):
        '''Dumps the queue as a generator and cleans it when done.
        '''

        while True:
            try:
                yield self.get()
            except QueueEmpty:
                break

    def empty(self):
        '''Returns True when queue and unacknowledged is empty otherwise False.'''

        return self.__q.empty()

    def enableFallthrough(self):
        self.put = self.__fallThrough

    def get(self):
        '''Gets an element from the queue.'''

        try:
            e = self.__q.pop()
        except IndexError:
            self.__empty.set()
            self.__full.clear()
            raise QueueEmpty("No more elements left to consume.", self.waitUntilFull, self.waitUntilContent)

        self.__out += 1
        self.__free.set()
        self.__content.clear()
        return e

    def rescue(self, element):

        self.__q.append(element)

    def size(self):
        '''Returns the length of the queue.'''

        return len(self.__q)

    def stats(self):
        '''Returns statistics of the queue.'''

        return {"size": len(self.__q),
                "in_total": self.__in,
                "out_total": self.__out,
                "in_rate": self.__rate("in_rate", self.__in),
                "out_rate": self.__rate("out_rate", self.__out),
                "dropped_total": self.__dropped,
                "dropped_rate": self.__rate("dropped_rate", self.__dropped)
                }

    def waitUntilEmpty(self):
        '''Blocks until the queue is completely empty.'''

        try:
            self.__empty.wait(timeout=0.1)
        except:
            pass

    def waitUntilFull(self):
        '''Blocks until the queue is completely full.'''

        try:
            self.__full.wait(timeout=0.1)
        except:
            pass

    def waitUntilFree(self):
        '''Blocks until at least 1 slot it free.'''

        try:
            self.__free.wait(timeout=0.1)
        except:
            pass

    def waitUntilContent(self):
        '''Blocks until at least 1 slot is taken.'''

        try:
            self.__content.wait(timeout=0.1)
        except:
            pass

    def __fallThrough(self, element):
        '''Accepts an element but discards it'''

        self.__dropped += 1

    def __put(self, element):
        '''Puts element in queue.'''

        if len(self.__q) == self.max_size:
            self.__empty.clear()
            self.__full.set()
            raise QueueFull("Queue has reached capacity of %s elements" % (self.max_size), self.waitUntilEmpty, self.waitUntilFree)

        self.__q.append(element)
        self.__in += 1
        self.__free.clear()
        self.__content.set()

    def __rate(self, name, value):

        if name not in self.__cache:
            self.__cache[name] = {"value": (time(), value), "rate": 0}
            return 0

        (time_then, amount_then) = self.__cache[name]["value"]
        (time_now, amount_now) = time(), value

        if time_now - time_then >= 1:
            self.__cache[name]["value"] = (time_now, amount_now)
            self.__cache[name]["rate"] = (amount_now - amount_then) / (time_now - time_then)

        return self.__cache[name]["rate"]
