# -*- coding: utf-8 -*-
from ZODB.POSException import ConflictError
from zope import component
from zope import interface
from zope.component.hooks import getSiteManager

import datetime
import logging
import persistent

logger = logging.getLogger('collective.pdfpeek.async')


class IQueue(interface.Interface):
    pass


class Queue(persistent.Persistent):
    interface.implements(IQueue)

    def __init__(self):
        self.pending = persistent.list.PersistentList()
        self.failures = persistent.list.PersistentList()
        self.finished = persistent.list.PersistentList()

    def process(self):
        num = len(self.pending)
        if num > 0:
            job = self.pending[0]
            try:
                job()
            except (ConflictError, KeyboardInterrupt):
                # Let Zope handle this.
                raise
            except:
                logger.warn(
                    'Removing job {0:s} after Exception:'.format(job),
                    exc_info=1
                )
                job.value = '{0:s} failed'.format(job)
                self.failures.append(job)
            else:
                logger.info('Finished job: {0:s}'.format(job))
                self.finished.append(job)
            self.pending.remove(job)
        return num


class Job(persistent.Persistent):
    executed = None
    title = u''

    def __init__(self, fun, *args, **kwargs):
        self._fun = fun
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        self.value = self._fun(*self._args, **self._kwargs)
        self.executed = datetime.datetime.now()

    def __str__(self):
        return '<Job {0:s} with args {1:s} and kwargs {2:s}>'.format(
            self._fun.__name__, self._args, self._kwargs)


def get_queue(name):
    queue = component.queryUtility(IQueue, name)
    if queue is None:
        queue = Queue()
        sm = getSiteManager()
        sm.registerUtility(queue, provided=IQueue, name=name)
    return queue
