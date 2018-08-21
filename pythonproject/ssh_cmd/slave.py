#!/usr/bin/python
import os
from Queue import Queue
from multiprocessing.managers import BaseManager
class Slave:
    def __init__(self):
        self.dispatched_job_queue = Queue()
        self.finished_job_queue = Queue()
    def start(self):
        BaseManager.register('get_dispatched_job_queue')
        BaseManager.register('get_finished_job_queue')
        server = '127.0.0.1'
        print('Connect to server %s...' % server)
        manager = BaseManager(address=(server, 8888), authkey='jobs')
        manager.connect()
        dispatched_jobs = manager.get_dispatched_job_queue()
        finished_jobs = manager.get_finished_job_queue()
        while not dispatched_jobs.empty():
            job = dispatched_jobs.get(timeout=1)
            print 'get cmd:',job
            result=os.popen(job).read().rstrip()
            finished_jobs.put(result)
if __name__ == "__main__":
        while True:
                slave = Slave()
                slave.start()