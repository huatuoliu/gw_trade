#!/usr/bin/python
# coding=utf-8
import urllib, urllib2, cookielib
import os,time,string
import sys
import logging

class trade_url:
    def __init__(self):
        self.my_cookie = ""

    #########################get html and base cookie ######################
    def prepare(self, first_url):
        tmp_cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(tmp_cookie))
        response = opener.open('https://trade.cgws.com/cgi-bin/user/Login?function=tradeLogout', timeout=5)
        for item in tmp_cookie:
            self.my_cookie+=item.name + "=" +item.value + ";"
        htm = response.read()
        return htm

    ########## post data to request_url ##############
    def post_to_url(self, request_url, post_data):
        post_encode = urllib.urlencode(post_data)
        #print post_encode
        req = urllib2.Request(
            url=request_url,
            data=post_encode
            )
        req.add_header('Cookie', self.my_cookie)
        #print req.headers
        #print req.data
        resp = urllib2.urlopen(req)
        htm = resp.read()
        return htm

    ########## get data to request_url ###############
    def get_to_url(self, request_url, get_data):
        if get_data == "":
            tmp_url = request_url
        else:
            tmp_url = request_url + "?" + get_data
        #print tmp_url
        #print self.my_cookie
        req = urllib2.Request(
            url=request_url,
            )
        req.add_header('Cookie', self.my_cookie)
        #print req.headers
        #print req.data
        try:
            resp = urllib2.urlopen(req, timeout=1)
        except urllib2.HTTPError, e:
            logging.warn("server process request error: err_code=%s", e.code)
            return 5, None
        except urllib2.URLError, e:
            logging.warn("reach server error: reason=%s", e.reason)
            return -10, None
        except Exception, e:
            logging.warn("reach server error: reason=%s", e.reason)
            return -10, None

        htm = resp.read()
        return htm
