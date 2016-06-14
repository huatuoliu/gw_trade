import threading
import time

class ProcessCondOrder(threading.Thread):
    def __init__(self, proc_id):
        threading.Thread.__init__(self)
        self.proc_id = proc_id #进程的id
        self.thread_stop = False #进程是否需要停止
        self.last_dbcheck_time = time.time() #最后一次查看db的时间


    #检查价格并且下单
    def check_price_do(self):


    #从数据库load数据到本地进行访问
    def load_from_db(self):


    def run(self):
        while not self.thread_stop:
            if self.last_dbcheck_time + 60 < time.time():
                load_from_db()
                self.last_dbcheck_time = time.time()
            check_price_do();

    def stop(self):
        self.thread_stop = True






