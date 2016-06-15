import threading
import time
from db_util import *

order_direction_def = {"up":1, "down":2}
order_state_def = {"todo":0, "done":1, "cancel":2}
order_action_def = {"buy":1, "sell":2}



class ProcessCondOrder(threading.Thread):
    def __init__(self, proc_id):
        threading.Thread.__init__(self)
        self.proc_id = proc_id #进程的id
        self.thread_stop = False #进程是否需要停止
        self.last_dbcheck_time = time.time() #最后一次查看db的时间
        self.todo_orders = None  #所有待触发的订单

    #检查价格并且下单
    def check_price_do(self):
        for row in self.todo_orders:
            now_price = get_now_price(row.stock_code)
            if now_price >= row.compare_price and  row.direction == order_direction_def["up"]:
                auto_trade.buy_sell()




    #从数据库load数据到本地进行访问
    def load_from_db(self):
        order_db = db_util()
        order_db.init_db()
        self.todo_orders = order_db.get_todo_orders()
        for row in self.todo_orders:
            print row.insert_time

    def run(self):
        while not self.thread_stop:
            if self.last_dbcheck_time + 60 < time.time():
                self.load_from_db()
                self.last_dbcheck_time = time.time()
            self.check_price_do();

    def stop(self):
        self.thread_stop = True






