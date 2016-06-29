# coding=utf-8
import os,time,string
import sys
import argparse
from trade_util import *
import logging

####### init log ################
logging.basicConfig(level=logging.DEBUG,
                format='[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='gw_trade.log',
                filemode='w')

#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


######## init parse #############
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--action_type", choices=['B', 'S', 'Q', 'A', 'G', 'C'], help="B: Buy; S: Sell; Q: Query Holdings; A: Query Account Info; G: Query Ongoings; C: Cancel Order")
parser.add_argument("cmd_args", nargs='*', help="[Buy Stock. Usage: -B stock_code price amount. e.g. -tB 600036  14.550 1000]" \
                                                "  [Sell Stock. Usage: -S  stock_code price amount. e.g. -tS 600036  14.550 1000]" \
                                                "  [Query Account Info. Usage: -tA]" \
                                                "  [Query Holding Stock. Usage: -tQ]" \
                                                "  [Query OnGoing Order. Usage: -tG]" \
                                                "  [Cancel OnGoing Order. Usage: -tC order_id. order_id can be acquired from the result of -tG cmd]")
args = parser.parse_args()
print args.action_type, args.cmd_args

auto_trade = auto_trade("config.ini")
ret = auto_trade.prepare()
if ret != 0:
    logging.warn("auto trade prepare fail: ret=%d" % ret)
    exit()

if (args.action_type == "B" or args.action_type == "S"):
    try:
        order_id = auto_trade.buy_sell(args.action_type, args.cmd_args[0], args.cmd_args[1],args.cmd_args[2])
        if order_id == "":
            logging.warn("Buy Or Sell Fail: order_id=%s" % order_id)
    except Exception, e:
        logging.warn("Exception = %s" % e.message)
        exit()

    print order_id
    #ongoing_list = auto_trade.query_ongoing_order()
    #time.sleep(10)
    #for  record in ongoing_list:
    #    auto_trade.cancel_order(record["order_id"])
elif (args.action_type == "Q"):
    (ret, result) = auto_trade.query_order()
    if ret != 0:
        logging.warn("query order fail: ret=%d" % ret)
    print result
elif (args.action_type == "A"):
    try:
        account_info = auto_trade.query_account()
    except Exception, e:
        print "Exception: msg=", e
        exit()
    print account_info
elif (args.action_type == "G"):
    try:
        ongoing_list = auto_trade.query_ongoing_order()
    except Exception, e:
        print "Exception: msg=", e
        exit()
    print ongoing_list
elif (args.action_type == "C"):
    try:
        auto_trade.cancel_order(args.cmd_args[0])
    except Exception, e:
        print "Exception: msg=", e
        exit()
else:
    print "No Such Action: " + args.action_type
#except Exception, e:
#    print "Process Error: e=" + e.message
#    exit(1)
#raw_input()


