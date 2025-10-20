from __future__ import annotations

import atexit
import queue
import threading

from app.models import Task
from app.process import QueueProcess


def status_handler(func):
    def wrapper(self, task_id, parameters):
        try:
            task = Task.objects.get(id=task_id)
            task.status = "processing"
            task.save()

            result = func(self, task.user, parameters)

            task.status = "completed"
            task.result = result
            task.save()

            return result
        except Exception as e:
            task.status = "failed"
            task.error_message = str(e)
            task.save()
            return None
    return wrapper


class TaskWorker(threading.Thread):
    def __init__(self, task_queue, worker_id):
        super().__init__(daemon=True)
        self.task_queue = task_queue
        self.worker_id = worker_id

    def start_and_get_thread(self):
        self.start()
        return self

    @status_handler
    def process_task(self, user, parameters):
        return QueueProcess().process(user, parameters)

    def run(self):
        while self.task_queue.keep_running():
            try:
                task_id, parameters = self.task_queue.get(timeout=1.0)
                if task_id is None:
                    break
            except queue.Empty:
                continue

            self.process_task(task_id, parameters)
            self.task_queue.task_done()


class TaskQueue:
    def __init__(self):
        self.inner_queue = queue.Queue()
        self.max_workers = 1
        self.shutdown_event = threading.Event()
        self.worker_threads = [TaskWorker(self, i).start_and_get_thread() for i in range(self.max_workers)]

    def put(self, task_id, parameters):
        self.inner_queue.put((task_id, parameters))

    def get(self, **kwargs):
        return self.inner_queue.get(**kwargs)

    def task_done(self):
        self.inner_queue.task_done()

    def keep_running(self):
        return not self.shutdown_event.is_set()

    def shutdown_workers(self):
        # Shutdown all worker threads gracefully
        self.shutdown_event.set()

        # Send shutdown signal to all workers
        for _ in self.worker_threads:
            self.put(None, None)

        # Wait for workers to finish
        for worker in self.worker_threads:
            worker.join(timeout=5.0)

        self.worker_threads.clear()


task_queue = TaskQueue()

atexit.register(lambda: task_queue.shutdown_workers())
