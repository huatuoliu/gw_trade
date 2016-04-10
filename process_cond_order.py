import threading
import time

class ProcessCondOrder(threading.Thread):
    def __init__(self, proc_id):
        threading.Thread.__init__(self)
        self.proc_id = proc_id
        self.thread_stop = False
        self.last_dbcheck_time = time.time()
        self.

    def check_price_do(self):
        #

    def load_from_db(self):
        #


    def run(self):
        while not self.thread_stop:
            if self.last_dbcheck_time + 60 < time.time():
                load_from_db()
                self.last_dbcheck_time = time.time()
            check_price_do();

    def stop(self):
        self.thread_stop = True






