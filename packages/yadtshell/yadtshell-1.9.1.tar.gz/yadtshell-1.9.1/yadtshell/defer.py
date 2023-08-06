#   YADT - an Augmented Deployment Tool
#   Copyright (C) 2010-2014  Immobilien Scout GmbH
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

import logging
import twisted.internet.defer as defer
import twisted.internet.reactor as reactor

import yadtshell.actions
import yadtshell.twisted


def next_in_queue(queue):
    # return queue.popleft()
    return queue.pop(0)


class DeferredPool(defer.Deferred):

    class Worker(object):

        def __init__(self, name, next_task_fun, handle_error_fun):
            self.next_task_fun = next_task_fun
            self.handle_error_fun = handle_error_fun
            self.name = name
            self.logger = logging.getLogger(name)
            self.stopped = False
            self.idle = True
            self.task = None

        def run(self, lastResult=None):
            if self.stopped:
                self.logger.debug('Worker stopped : %s' % self.__str__())
                return None
            task = self.next_task_fun()
            self.task = task
            if not task:
                self.idle = True
                reactor.callLater(1, self.run)
                return None
            self.idle = False
            self.logger.debug('starting %s(..)' % task.fun.__name__)
            # TODO: plan = action?
            d = task.fun(plan=task.action, path=task.path)
            d.addErrback(self.handle_error_fun)
            d.addErrback(yadtshell.twisted.report_error, self.logger.error)
            d.addBoth(self.run)
            return d

        def __str__(self):
            try:
                action = self.task.action
            except:
                action = "None"
            return "worker[%s], stopped: %s, idle: %s, action: %s" % (self.name, self.stopped, self.idle, action)

    def __init__(self, name, queue, nr_workers=1, next_task_fun=next_in_queue, nr_errors_tolerated=0):
        defer.Deferred.__init__(self)
        self.name = name
        self.next_task_fun = next_task_fun
        self.nr_errors_tolerated = int(nr_errors_tolerated)
        self.error_count = 0
        self.logger = logging.getLogger('%s' % self.name)
        self.queue = queue
        if not queue:
            reactor.callLater(0, self.callback)
            return
        self.workers = [self.Worker('%s_worker%i' % (self.name, nr), self._next_task, self._handle_error)
                        for nr in range(0, nr_workers)]
        if nr_workers > 1:
            self.logger.debug(
                'started: %i items in queue, %i parallel workers' % (len(queue), nr_workers))
        else:
            self.logger.debug('started: %i items in queue' % len(queue))
        for worker in self.workers:
            worker.run()

    def _finish(self):
        self.logger.debug('DeferredPool %s fired its callback.' % self.name)
        if self.error_count > self.nr_errors_tolerated:
            reactor.callLater(0, self.errback, yadtshell.actions.ActionException(
                'stops: error count too high, %i > %i' % (self.error_count, self.nr_errors_tolerated), 1))
            return
        if self.queue:
            self.logger.error(
                '%i actions not executed, dump follows:' % len(self.queue))
            for task in self.queue:
                for line in task.action.dump().splitlines():
                    self.logger.error(line)
            reactor.callLater(0, self.errback, yadtshell.actions.ActionException(
                'Could not execute %i action(s)' % len(self.queue), 1))
            return
        # TODO refactor to something similar to deferredList
        return self.callback(None)

    def _handle_error(self, failure):
        self.error_count += 1
        if self.error_count > self.nr_errors_tolerated:
            self._stop_workers()
            return failure
        self.logger.warn(
            'error encountered, error count: %i <= %i, continuing...' %
            (self.error_count, self.nr_errors_tolerated))
        return failure.value.orig_protocol

    def _next_task(self):
        if self.called:
            return None
        if len(self.queue) == 0:
            if not self.all_workers_idle():
                return None
            self.logger.debug(
                'Queue is empty and all worker are idle, thus closing pool instance.')
            self._stop_workers()
            return None
        fun = self.next_task_fun
        task = fun(self.queue)
        if not task:
            if self.all_workers_idle():
                self.logger.debug(
                    'Queue is not empty, but all workers are idle and no tasks are available. Thus stopping.')
                for worker in self.workers:
                    self.logger.debug("stopping %s" % worker)
                self._stop_workers()
                return None
        return task

    def _stop_workers(self):
        self.logger.debug('Stopping all workers..')
        for worker in self.workers:
            worker.stopped = True
        if not self.called:
            self._finish()

    def all_workers_idle(self):
        for worker in self.workers:
            if not worker.idle:
                return False
        return True
