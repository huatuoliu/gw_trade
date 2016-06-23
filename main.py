# coding=utf-8
import os,time,string
import sys
import argparse
from trade_util import *

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

try:
    auto_trade = auto_trade("config.ini")
except Exception, e:
        print "Exception: msg=", e
        exit()

if (args.action_type == "B" or args.action_type == "S"):
    try:
        order_id = auto_trade.buy_sell(args.action_type, args.cmd_args[0], args.cmd_args[1],args.cmd_args[2])
        if order_id == "":
            print "Buy Or Sell Fail"
    except Exception, e:
        print "Exception: msg=", e
        exit()

    print order_id
    #ongoing_list = auto_trade.query_ongoing_order()
    #time.sleep(10)
    #for  record in ongoing_list:
    #    auto_trade.cancel_order(record["order_id"])
elif (args.action_type == "Q"):
    try:
        holdings = auto_trade.query_order()
    except Exception, e:
        print "Exception: msg=", e
        exit()
    print holdings
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


