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
                filemode='a')

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
parser.add_argument("cmd_args", nargs='*', help="[Buy Stock. Usage: -B stock_code price amount. e.g. -tB 159915  2 100]" \
                                                "  [Sell Stock. Usage: -S  stock_code price amount. e.g. -tS 159915 2 100]" \
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
    (ret, result) = auto_trade.buy_sell(args.action_type, args.cmd_args[0], args.cmd_args[1],args.cmd_args[2])
    if ret == 0:
        logging.info("Deal OK: order_id=%s" % result)
    else:
        logging.warn("Buy Or Sell Fail: ret=%d, ret_msg=%s" % (ret, result))
    #ongoing_list = auto_trade.query_ongoing_order()
    #time.sleep(10)
    #for  record in ongoing_list:
    #    auto_trade.cancel_order(record["order_id"])
elif (args.action_type == "Q"):
    (ret, result) = auto_trade.query_order()
    if ret == 0:
        logging.info("Query holdings OK: result=%s" % result)
    else:
        logging.warn("query order fail: ret=%d" % ret)
elif (args.action_type == "A"):
    (ret, result) = auto_trade.query_account()
    if ret == 0:
        logging.info("Query account OK: result=%s" % result)
    else:
        logging.warn("query account fail: ret=%d" % ret)
elif (args.action_type == "G"):
    (ret, result) = auto_trade.query_ongoing_order()
    if ret == 0:
        logging.info("Query Ongoing Order OK: result=%s" % result)
    else:
        logging.warn("query ongoing order fail: ret=%d" % ret)

elif (args.action_type == "C"):
    (ret, result) = auto_trade.cancel_order(args.cmd_args[0])
    if ret == 0:
        logging.info("Cancel Order OK: order_id=%s" % args.cmd_args[0])
    else:
        logging.warn("query cancel order fail: ret=%d, msg=%s" % (ret, result))
else:
    print "No Such Action: " + args.action_type
#except Exception, e:
#    print "Process Error: e=" + e.message
#    exit(1)
#raw_input()


