#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 05:39:15 2017

@author: frank
"""
from urllib import request
import logging

FORMAT = '%(asctime)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("scrawlog")
logger.setLevel(logging.INFO)
USER_AGENT = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

class stock_cols:
    ID = 'id'
    NAME = 'name'
    TOTAL_CAPITAL = 'total_capital'
    CURRENT_CAPITAL = 'current_capital'
    AVERAGE_VOLUME_LAST_5_DAYS = 'average_volume_last_5_days'
    PRICE_5_AGO = 'price_5_ago'
    PRICE_10_AGO = 'price_10_ago'
    PRICE_20_AGO = 'price_20_ago'
    PRICE_60_AGO = 'price_60_ago'
    PRICE_120_AGO = 'price_120_ago'
    PRICE_250_AGO = 'price_250_ago'
    PROFIT = 'profit'
    GRADELEVEL = 'gradelevel'
    GRADEAMT = 'gradeamt'
    TODAY_OPEN_PRICE = 'today_open_price'
    YESTERDAY_CLOSE_PRICE = 'yesterday_close_price'
    TODAY_CLOSE_PRICE = 'today_close_price'
    HIGH_PRICE = 'high_price'
    LOW_PRICE = 'low_price'
    VOLUME = 'volume'
    TURNOVER = 'turnover'
    BUY_1_NUM = 'buy_1_num'
    BUY_1_PRICE = 'buy_1_price'
    BUY_2_NUM = 'buy_2_num'
    BUY_2_PRICE = 'buy_2_price'
    BUY_3_NUM = 'buy_3_num'
    BUY_3_PRICE = 'buy_3_price'
    BUY_4_NUM = 'buy_4_num'
    BUY_4_PRICE = 'buy_4_price'
    BUY_5_NUM = 'buy_5_num'
    BUY_5_PRICE = 'buy_5_price'
    SELL_1_NUM = 'sell_1_num'
    SELL_1_PRICE = 'sell_1_price'
    SELL_2_NUM = 'sell_2_num'
    SELL_2_PRICE = 'sell_2_price'
    SELL_3_NUM = 'sell_3_num'
    SELL_3_PRICE = 'sell_3_price'
    SELL_4_NUM = 'sell_4_num'
    SELL_4_PRICE = 'sell_4_price'
    SELL_5_NUM = 'sell_5_num'
    SELL_5_PRICE = 'sell_5_price'
    TOTAL_SHARE_CAPITAL = 'total_share_capital'
    OUTSTANDING_SHARES = 'outstanding_shares'
    PRICE_HIST = "price_hist"
    AREA = 'area'
    AREA_RATE = 'area_rate'
    DATE = 'date'
    MAIN_BUY = 'main_buy'
    FOLLOW_BUY = 'follow_buy'
    RETAIL_BUY = 'retail_buy'
    MAIN_BUY_5_DAYS = 'main_buy_5_days'
    MAIN_BUY_10_DAYS = 'main_buy_10_days'

def get_logger():
    return logger

def craw_web_content(url):
    logger.debug("start crawl " + url)
    req = request.Request(url)
    req.add_header('User-agent', USER_AGENT)
    resp = request.urlopen(url)
    if resp is None:
        logger.warning("response for {} is null".format(url))
        return None
    raw_resp = resp.read()
    if raw_resp is None:
        logger.warning("raw response for {} is null or empty".format(url))
        return None
    resp_str = str(raw_resp, encoding='gbk')
    logger.debug("get response from " + url)
    return resp_str