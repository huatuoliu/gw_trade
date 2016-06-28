#!/usr/bin/python
# coding=utf-8
import urllib, urllib2, cookielib
import os,time,string
import sys
import re
import random
from trade_url import *
import ConfigParser
# from crack_vc import crack_vc
from stock_util import *
from html_parser import *
from crack_bmp import *
import logging

class auto_trade:
    def __init__(self, config_file):
        self.account = ""
        self.passwd_encrypted = ""
        self.secuids = None
        self.stock_code = ""
        self.order_type = ""
        self.price = ""
        self.amount = ""
        self.read_config(config_file)
        self.gw_trade = trade_url()
        self.prepare()

    def read_config(self, config_file):
        #读取配置文件
        cf = ConfigParser.ConfigParser()
        try:
            cf.read(config_file)
            self.account = cf.get("common", "account")
            self.passwd_encrypted = cf.get("common", "passwd_encrypted") #加密后的密码
            secuids_sh = cf.get("common", "secuids_sh")  #上海的股东代码
            secuids_sz = cf.get("common", "secuids_sz") #深圳的股东代码
            self.secuids = {
                        1: secuids_sh,
                        0: secuids_sz
                    }
        except Exception, e:
            #logging.warning()
            return

    # 登录后获得cookie
    def prepare(self):
        ###preprea for login
        self.gw_trade.prepare("https://trade.cgws.com/cgi-bin/user/Login?function=tradeLogout")
        #get verify code
        #urllib.urlretrieve("https://trade.cgws.com/cgi-bin/img/validateimg", "d://1.jpg", None)
        tmp_buff = self.gw_trade.get_to_url("https://trade.cgws.com/cgi-bin/img/validateimg", "rand=" + str(random.random()))
        #tmp_buff = gw_trade.get_to_url("https://trade.cgws.com/cgi-bin/img/validateimg", "")0
        verify_pic = open('d://1.jpg', 'wb')
        verify_pic.write(tmp_buff)
        verify_pic.close()
        #verify_code = crack_vc().get_vcode(r"d:\1.jpg", r"d:\vcode")
        crack_bmp1 = crack_bmp()
        verify_code = crack_bmp1.decode_from_file("d://1.jpg")
        #pasre verify code,just input by you
        #verify_code = raw_input('Enter verify code : ')
        #print verify_code

        ##################login######################
        post_data={
        'ticket': verify_code,
        'retUrl':'',
        'password': self.passwd_encrypted,
        'mac': '',
        'password_Controls': 'normal',
        'type':'Z',
        'fundAccount': self.account,
        'isSaveAccount':'1',
        'normalpassword':'',
        }
        ret = self.gw_trade.post_to_url("https://trade.cgws.com/cgi-bin/user/Login", post_data)
        #print ret
        ############ get main page cookie ##############

    #买卖
    #输入参数：
    def buy_sell(self, order_type,  stock_code, price, amount):
        print "Action of ", stock_code , ": Order_type=", order_type , ", price=" , price , ", amount=" , amount
        ############ post buy order #######################
        stock_ut = stock_util()
        market_id  = stock_ut.get_market(stock_code)
        up_limit = stock_ut.get_up_limit(price)
        down_limit = stock_ut.get_down_limit(price)
        #print market_id
        secuid = self.secuids[market_id]
        maxBuy = 0
        post_data = {
        "type": order_type,
        "market": market_id,
        "up_limit": up_limit,
        "down_limit": down_limit,
        "stktype": "0",
        "secuid": secuid,
        "stkcode": stock_code,
        "stockName":"",
        "price": price,
        "fundavl": "1.00",
        "maxBuy": maxBuy,
        "amount": amount
        }
        ret = self.gw_trade.post_to_url("https://trade.cgws.com/cgi-bin/stock/StockEntrust?function=StockBusiness", post_data)
        #解析出合同编号，如果出错，那么返回""
        #print ret

        #150906130资金不足
        #150906135股数不够
        #长城的出错都是这个鸟样 alert("-990297020[-990297020]，出错了就反馈空的订单号，看看是不是自己定义一些exception来搞
        reg = re.compile(ur'alert.*?(-\d+)')
        match = reg.search(ret)
        if match:
            logging.warn("Deal Order Fail: match=%s" % match)
            return ""

        #ok，没有问题
        reg = re.compile(ur'alert.*(\d{4})')
        match = reg.search(ret)
        if match:
            return match.group(1)
        else:
            return ""

    def cancel_order(self, order_id):
        ##print "Action of " + stock_code + ": Order_type=" + order_type + ", price=" + price + ", amount=" + amount
        ############ post buy order #######################
        post_data={
        "id": order_id
        }
        ret = self.gw_trade.post_to_url("https://trade.cgws.com/cgi-bin/stock/StockEntrust?function=StockCancel", post_data)
        print ret
        return

    def query_account(self):
        tmp_buff = self.gw_trade.get_to_url("https://trade.cgws.com/cgi-bin/stock/EntrustQuery?function=MyAccount", "")
        #print tmp_buff
        html_parse_inst = html_parser(tmp_buff)
        return html_parse_inst.get_account()

    def query_order(self):
        tmp_buff = self.gw_trade.get_to_url("https://trade.cgws.com/cgi-bin/stock/EntrustQuery?function=MyStock&stktype=0", "")
        #print tmp_buff
        html_parse_inst = html_parser(tmp_buff)
        return html_parse_inst.get_holdings()

    ################# query ongoing order ####################
    def query_ongoing_order(self):
        print "........... query ongoing order ................"
        tmp_buff = self.gw_trade.get_to_url("https://trade.cgws.com/cgi-bin/stock/StockEntrust?function=StockCancel", "")
        html_parse_inst = html_parser(tmp_buff)
        print "........... query order finish ................."
        return html_parse_inst.get_onging_orders()









