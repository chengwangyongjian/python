#!/usr/bin/python
from Queue import Queue
from multiprocessing.managers import BaseManager
class Master:
    def __init__(self):
        self.dispatched_job_queue = Queue()
        self.finished_job_queue = Queue()
    def get_dispatched_job_queue(self):
        return self.dispatched_job_queue
    def get_finished_job_queue(self):
        return self.finished_job_queue
    def start(self):
        BaseManager.register('get_dispatched_job_queue', callable=self.get_dispatched_job_queue)
        BaseManager.register('get_finished_job_queue', callable=self.get_finished_job_queue)
        manager = BaseManager(address=('0.0.0.0', 8888), authkey='jobs')
        manager.start()
        dispatched_jobs = manager.get_dispatched_job_queue()
        finished_jobs = manager.get_finished_job_queue()
        dispatched_jobs.put(cmd)
        while not dispatched_jobs.empty():
              job = finished_jobs.get()
              print 'result:',job
        manager.shutdown()
if __name__ == "__main__":
        while True:
                cmd=raw_input('cmd:')
                master = Master()
                master.start()
