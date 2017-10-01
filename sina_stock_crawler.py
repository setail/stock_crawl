#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 05:36:59 2017

@author: frank
"""
import re
import time
import globl
from datetime import date
import datetime
from globl import stock_cols

logger = globl.get_logger()
static_url_pattern = "http://finance.sina.com.cn/realstock/company/{0}/nc.shtml"
realtime_url_pattern = "http://hq.sinajs.cn/rn={0}&list={1},{1}_i,bk_{2}"
price_hist_url_pattern = "http://market.finance.sina.com.cn/pricehis.php?symbol={}&startdate={}&enddate={}"
stock_pattern = re.compile("var hq_str_[\w\d]{8}=\"(.*?)\";")
stock_i_pattern = re.compile("var hq_str_[\w\d]{8}_i=\"(.*?)\";")
bk_jdly_pattern = re.compile("var hq_str_bk_new_\w+=\"(.*?)\"")

def craw_stock_price_hist(stock_id):
    today = date.today()
    start_date = today - datetime.timedelta(30)
    return globl.craw_web_content(price_hist_url_pattern.format(stock_id, start_date, today))

def parse_stock_price_hist_content(content, stock):
    price_hist_list = re.findall('<td>([.\d]+)</td>\s*<td>(\d+)</td>\s*<td>([.\d]+%)</td>', content)
    res = ";".join([":".join(i) for i in price_hist_list])
    stock[stock_cols.PRICE_HIST] = res

def craw_stock_static_data(stock_id):
    url = static_url_pattern.format(stock_id)
    return globl.craw_web_content(url)

def __get_match_value(match_obj, i):
    return match_obj.group(1) if match_obj is not None else ""

def parse_sine_static_stock_content(content, stock):
    matches = re.search("<h1 id=\"stockName\">(.+)<span>", content)
    stock[stock_cols.NAME] = __get_match_value(matches, 1)
    matches = re.search("var totalcapital\s*=\s*([\d.]+);", content)
    stock[stock_cols.TOTAL_CAPITAL] = __get_match_value(matches, 1)
    matches = re.search("var currcapital\s*=\s*([\d.]+);", content)
    stock[stock_cols.CURRENT_CAPITAL] = __get_match_value(matches, 1)
    matches = re.search("var lastfive\s*=\s*([\d.]+);", content)
    stock[stock_cols.AVERAGE_VOLUME_LAST_5_DAYS] = __get_match_value(matches, 1)
    matches = re.search("var price_5_ago\s*=\s*([\d.]+);", content)
    stock[stock_cols.PRICE_5_AGO] = __get_match_value(matches, 1)
    matches = re.search("var price_10_ago\s*=\s*([\d.]+);", content)
    stock[stock_cols.PRICE_10_AGO] = __get_match_value(matches, 1)
    matches = re.search("var price_20_ago\s*=\s*([\d.]+);", content)
    stock[stock_cols.PRICE_20_AGO] = __get_match_value(matches, 1)
    matches = re.search("var price_60_ago\s*=\s*([\d.]+);", content)
    stock[stock_cols.PRICE_60_AGO] = __get_match_value(matches, 1)
    matches = re.search("var price_120_ago\s*=\s*([\d.]+);", content)
    stock[stock_cols.PRICE_120_AGO] = __get_match_value(matches, 1)
    matches = re.search("var price_250_ago\s*=\s*([\d.]+);", content)
    stock[stock_cols.PRICE_250_AGO] = __get_match_value(matches, 1)
    matches = re.search("var profit\s*=\s*([\d.]+);", content)
    stock[stock_cols.PROFIT] = __get_match_value(matches, 1)
    matches = re.search("var gradeLevel\s*=\s*([\d.]+);", content)
    stock[stock_cols.GRADELEVEL] = __get_match_value(matches, 1)#评级
    matches = re.search("var gradeAmt\s*=\s*([\d.]+);", content)
    stock[stock_cols.GRADEAMT] = __get_match_value(matches, 1)#评级机构

def craw_stock_realtime_data(stock_id, area):
    url = realtime_url_pattern.format(int(time.time() * 1000), stock_id, area)
    return globl.craw_web_content(url)

def parse_sina_realtime_stock_content(content, stock):
    matches = stock_pattern.search(content)
    info = matches.group(1).split(",") if matches is not None and matches.lastindex > 0 else []
    __set_value(stock, stock_cols.TODAY_OPEN_PRICE, info, 1)
    __set_value(stock, stock_cols.YESTERDAY_CLOSE_PRICE, info, 2)
    __set_value(stock, stock_cols.TODAY_CLOSE_PRICE, info, 3)
    __set_value(stock, stock_cols.HIGH_PRICE, info, 4)
    __set_value(stock, stock_cols.LOW_PRICE, info, 5)
    __set_value(stock, stock_cols.VOLUME, info, 8)
    __set_value(stock, stock_cols.TURNOVER, info, 9)
    
    __set_value(stock, stock_cols.BUY_1_NUM, info, 10)
    __set_value(stock, stock_cols.BUY_1_PRICE, info, 11)
    __set_value(stock, stock_cols.BUY_2_NUM, info, 12)
    __set_value(stock, stock_cols.BUY_2_PRICE, info, 13)
    __set_value(stock, stock_cols.BUY_3_NUM, info, 14)
    __set_value(stock, stock_cols.BUY_3_PRICE, info, 15)
    __set_value(stock, stock_cols.BUY_4_NUM, info, 16)
    __set_value(stock, stock_cols.BUY_4_PRICE, info, 17)
    __set_value(stock, stock_cols.BUY_5_NUM, info, 18)
    __set_value(stock, stock_cols.BUY_5_PRICE, info, 19)
    
    __set_value(stock, stock_cols.SELL_1_NUM, info, 20)
    __set_value(stock, stock_cols.SELL_1_PRICE, info, 21)
    __set_value(stock, stock_cols.SELL_2_NUM, info, 22)
    __set_value(stock, stock_cols.SELL_2_PRICE, info, 23)
    __set_value(stock, stock_cols.SELL_3_NUM, info, 24)
    __set_value(stock, stock_cols.SELL_3_PRICE, info, 25)
    __set_value(stock, stock_cols.SELL_4_NUM, info, 26)
    __set_value(stock, stock_cols.SELL_4_PRICE, info, 27)
    __set_value(stock, stock_cols.SELL_5_NUM, info, 28)
    __set_value(stock, stock_cols.SELL_5_PRICE, info, 29)
    __set_value(stock, stock_cols.DATE, info, 30)
    matches = stock_i_pattern.search(content)
    info = matches.group(1).split(",") if matches is not None and matches.lastindex > 0 else []
    __set_value(stock, stock_cols.TOTAL_SHARE_CAPITAL, info, 7)
    __set_value(stock, stock_cols.OUTSTANDING_SHARES, info, 8)
    matches = bk_jdly_pattern.search(content)
    # area info
    info = matches.group(1).split(",") if matches is not None and matches.lastindex > 0 else []
    __set_value(stock, stock_cols.AREA, info, 1)
    __set_value(stock, stock_cols.AREA_RATE, info, 5)
    return stock

def __set_value(d, k, info, index):
    d[k] = info[index] if info is not None and len(info) > index else ""

def crawl_stock_data(stk, stock_id):
    main_content = craw_stock_static_data(stock_id)
    parse_sine_static_stock_content(main_content, stk)
    matches = re.search("var bkSymbol\s*=\s*'([\w_]+)';", main_content)
    area = __get_match_value(matches, 1)
    realtime_content = craw_stock_realtime_data(stock_id, area)
    parse_sina_realtime_stock_content(realtime_content, stk)
    parse_stock_price_hist_content(craw_stock_price_hist(stock_id), stk)
    return stk