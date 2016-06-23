# coding:utf-8
import threading
import time
from db_util import *
from ftnn_api import *
from stock_util import *
from trade_util import *

order_direction_def = {"up":1, "down":2}
order_state_def = {"todo":0, "done":1, "cancel":2}
order_action_def = {"B":1, "S":2}


class process_cond_order():
    def __init__(self):
        self.last_dbcheck_time = 0 #最后一次查看db的时间
        self.todo_orders = None  #所有待触发的订单
        self.order_db = db_util()
        self.order_db.init_db()
        self.auto_trade = auto_trade("config.ini")

    #检查价格并且下单
    def check_price_do(self):
        ft_api = Futu()
        for row in self.todo_orders:
            xs_data  = ft_api.get_ticker(stock_util().get_market_name(row.stock_code), row.stock_code)
            now_price = xs_data['Cur']
            print "now_price=", now_price, ", row_compare_price=", row.compare_price, ", row.direction=", row.direction
            if now_price >= row.compare_price and  row.direction == order_direction_def["up"] \
                    or  now_price <= row.compare_price and  row.direction == order_direction_def["down"]:
                print "row.order_id=", row.order_id, "row.action = ", row.action, ", row.deal_price=", row.deal_price, ", row.amount=", row.amount
                self.auto_trade.buy_sell(row.action, row.stock_code, row.deal_price, row.amount)
                self.order_db.update_cond_order(row.order_id, order_state_def["done"])

    #从数据库load数据到本地进行访问
    def load_from_db(self):
        self.todo_orders = self.order_db.get_todo_orders()
        for row in self.todo_orders:
            print "stock_code=", row.stock_code, ", insert_time=", row.insert_time

    def run(self):
        while True:
            if self.last_dbcheck_time + 60 < time.time():
                self.load_from_db()
                self.last_dbcheck_time = time.time()
            self.check_price_do()
            time.sleep(5)

process = process_cond_order()
process.run()



