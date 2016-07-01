# coding:utf-8
import threading
import time
from db_util import *
from ftnn_api import *
from stock_util import *
from trade_util import *

####### init log ################
logging.basicConfig(level=logging.DEBUG,
                format='[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='proc_cond_order.log',
                filemode='a')

#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################




class process_cond_order():
    def __init__(self):
        self.last_dbcheck_time = 0 #最后一次查看db的时间
        self.todo_orders = None  #所有待触发的订单
        self.order_db = db_util()
        self.order_db.init_db()
        self.auto_trade = auto_trade("config.ini")
        ret = self.auto_trade.prepare()
        if ret != 0:
            logging.warn("auto trade prepare fail: ret=%d" % ret)
            return None

    #检查价格并且下单
    def check_price_do(self):
        ft_api = Futu()
        for row in self.todo_orders:
            xs_data  = ft_api.get_ticker(stock_util().get_market_name(row.stock_code), row.stock_code)
            now_price = xs_data['Cur']
            logging.info("Checking Cond Order: now_price=%d, row_compare_price=%f, row.direction=%s" % (now_price, row.compare_price, row.direction))
            if now_price >= row.compare_price and row.direction == order_direction_def["up"] \
                    or  now_price <= row.compare_price and row.direction == order_direction_def["down"]:
                logging.info("submit order: row.order_id=%s, row.action =%s, , row.deal_price=%f,  row.amount=%d" % (row.order_id, row.action, row.deal_price,  row.amount))
                (ret, result) = self.auto_trade.buy_sell(row.action, row.stock_code, row.deal_price, row.amount)
                if ret != 0:
                    logging.warn("deal fail: ret=%d, action=%s, stock_code=%s, deal_price=%f, amount=%d" % (ret, row.action, row.stock_code, row.deal_price, row.amount))
                    continue
                self.order_db.update_cond_order(row.order_id, order_state_def["done"])

    #从数据库load数据到本地进行访问
    def load_from_db(self):
        self.todo_orders = self.order_db.get_todo_orders()
        for row in self.todo_orders:
            logging.info( "Load from db: stock_code=%s, , insert_time=%s" %(row.stock_code, row.insert_time))

    def run(self):
        while True:
            if self.last_dbcheck_time + 60 < time.time():
                self.load_from_db()
                self.last_dbcheck_time = time.time()
            self.check_price_do()
            time.sleep(5)


process = process_cond_order()
process.run()



