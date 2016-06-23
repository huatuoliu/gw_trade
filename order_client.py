# coding=utf-8
import os,time,string
import sys
import argparse
import xmlrpclib
proxy = xmlrpclib.ServerProxy("http://localhost:8000/")
#print str(proxy.is_even(12))
#proxy.add_condition_order("600036", 1, 1, 100, 17, 2, 3)


######## init parse #############
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--action_type", choices=['B', 'S', 'Q', 'G', 'C'], help="B: Buy; S: Sell; Q: All Cond Order; G: Query Ongoing Cond Order; C: Cancel Order")
parser.add_argument("cmd_args", nargs='*', help="[Buy Cond Order. Usage: -B stock_code direction compare_price deal_price amount  begin_in_day end_in_day. e.g. -tB 159915 U 2.0 2.02 100 1430 1500]" \
                                                "  [Sell Cond Order. Usage: -S  stock_code direction compare_price deal_price amount  begin_in_day end_in_day. e.g. -tB 159915 D 2.0 2.02 100 1430 1500]" \
                                                "  [Query All Cond Order. Usage: -tQ stock_code]" \
                                                "  [Query Ongoing Cond Order. Usage: -tG stocke_code]" \
                                                "  [Cancel Cancel Order. Usage: -tC order_id. order_id can be acquired from the result of -tG cmd]")
args = parser.parse_args()
print args.action_type, args.cmd_args

if (args.action_type == "B" or args.action_type == "S"):
    try:
        proxy.add_condition_order(args.cmd_args[0], args.cmd_args[1], args.cmd_args[2], args.action_type, args.cmd_args[3], args.cmd_args[4], args.cmd_args[5], args.cmd_args[6])
    except Exception, e:
        print "Exception: msg=", e
        exit()
    #ongoing_list = auto_trade.query_ongoing_order()
    #time.sleep(10)
    #for  record in ongoing_list:
    #    auto_trade.cancel_order(record["order_id"])
elif (args.action_type == "Q"):
    try:

        if len(args.cmd_args) == 0:
            stock_code = ""
        else:
            stock_code = args.cmd_args[0]
        order_list = proxy.get_all_orders(stock_code)
    except Exception, e:
        print "Exception: msg=", e
        exit()
    print order_list
elif (args.action_type == "G"):
    try:
        if len(args.cmd_args) == 0:
            stock_code = ""
        else:
            stock_code = args.cmd_args[0]
        order_list = proxy.get_todo_orders(stock_code)
    except Exception, e:
        print "Exception: msg=", e
        exit()
    print order_list
elif (args.action_type == "C"):
    try:
        proxy.cancel_cond_order(args.cmd_args[0])
    except Exception, e:
        print "Exception: msg=", e
        exit()
else:
    print "No Such Action: " + args.action_type


