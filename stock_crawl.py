#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 21:56:27 2017

@author: frank
"""
from urllib import request
import logging
import time
import argparse
from datetime import date
from collections import OrderedDict
import sys
import os
import re
LOG = "./log"
OUTPUT_DIR = "./data"
INPUT_FILE = "./data/all_stock_ids"
FORMAT = '%(asctime)-8s %(message)s'
MAX_RETRY = 3
logging.basicConfig(filename = LOG, format=FORMAT)
logger = logging.getLogger("scrawlog")
logger.setLevel(logging.DEBUG)
static_url_pattern = "http://finance.sina.com.cn/realstock/company/{0}/nc.shtml"
realtime_url_pattern = "http://hq.sinajs.cn/rn={0}&list={1},{1}_i,bk_new_jdly"
stock_pattern = re.compile("var hq_str_[\w\d]{8}=\"(.*?)\";")
stock_i_pattern = re.compile("var hq_str_[\w\d]{8}_i=\"(.*?)\";")
bk_jdly_pattern = re.compile("var hq_str_bk_new_jdly=\"(.*?)\"")


class stock:
    pass

def craw_stock_content(url):
    resp = request.urlopen(url)
    if resp is None:
        logger.warning("response for {} is null".format(url))
        return None
    raw_resp = resp.read()
    if raw_resp is None:
        logger.warning("raw response for {} is null or empty".format(url))
        return None
    resp_str = str(raw_resp, encoding='gbk')
    return resp_str

def craw_stock_static_data(stock_id):
    url = static_url_pattern.format(stock_id)
    return craw_stock_content(url)

def parse_sine_static_stock_content(content, stock):
    matches = re.search("var totalcapital\s*=\s*([\d.]+);", content)
    stock["total_capital"] = matches.group(1)
    matches = re.search("var currcapital\s*=\s*([\d.]+);", content)
    stock["current_capital"] = matches.group(1)
    matches = re.search("var lastfive\s*=\s*([\d.]+);", content)
    stock["average_volume_last_5_days"] = matches.group(1)
    matches = re.search("var price_5_ago\s*=\s*([\d.]+);", content)
    stock["price_5_ago"] = matches.group(1)
    matches = re.search("var price_10_ago\s*=\s*([\d.]+);", content)
    stock["price_10_ago"] = matches.group(1)
    matches = re.search("var price_20_ago\s*=\s*([\d.]+);", content)
    stock["price_20_ago"] = matches.group(1)
    matches = re.search("var price_60_ago\s*=\s*([\d.]+);", content)
    stock["price_60_ago"] = matches.group(1)
    matches = re.search("var profit\s*=\s*([\d.]+);", content)
    stock["profit"] = matches.group(1)
    matches = re.search("var gradeLevel\s*=\s*([\d.]+);", content)
    stock["gradeLevel"] = matches.group(1)#评级
    matches = re.search("var gradeAmt\s*=\s*([\d.]+);", content)
    stock["gradeAmt"] = matches.group(1)#评级机构

def craw_stock_realtime_data(stock_id):
    url = realtime_url_pattern.format(int(time.time() * 1000), stock_id)
    return craw_stock_content(url)

def parse_sina_realtime_stock_content(content, stock):
    matches = stock_pattern.search(content)
    if matches == None or matches.lastindex < 1:
        logger.warning("cannot find match stock_pattern from content : " + content)
        return None
    info = matches.group(1).split(",")
    stock["name"] = info[0]
    stock["today_open_price"] = info[1]
    stock["yesterday_close_price"] = info[2]
    stock["today_close_price"] = info[3]
    stock["high_price"] = info[4]
    stock["low_price"] = info[5]
    stock["volume"] = info[8]
    stock["turnover"] = info[9]
    
    stock["buy_1_num"] = info[10]
    stock["buy_1_price"] = info[11]
    stock["buy_2_num"] = info[12]
    stock["buy_2_price"] = info[13]
    stock["buy_3_num"] = info[14]
    stock["buy_3_price"] = info[15]
    stock["buy_4_num"] = info[16]
    stock["buy_4_price"] = info[17]
    stock["buy_5_num"] = info[18]
    stock["buy_5_price"] = info[19]
    
    stock["sell_1_num"] = info[20]
    stock["sell_1_price"] = info[21]
    stock["sell_2_num"] = info[22]
    stock["sell_2_price"] = info[23]
    stock["sell_3_num"] = info[24]
    stock["sell_3_price"] = info[25]
    stock["sell_4_num"] = info[26]
    stock["sell_4_price"] = info[27]
    stock["sell_5_num"] = info[28]
    stock["sell_5_price"] = info[29]
    matches = stock_i_pattern.search(content)
    if matches == None or matches.lastindex < 1:
        logger.warning("cannot find match stock_i_pattern from content : " + content)
        return None
    info = matches.group(1).split(",")
    stock["total_share_capital"] = info[7]
    stock["outstanding_shares"] = info[8]
    return stock

def crawl_stock(stock_id):
    stk = OrderedDict()
    stk['id'] = stock_id
    realtime_content = craw_stock_realtime_data(stock_id)
    parse_sina_realtime_stock_content(realtime_content, stk)
    main_content = craw_stock_static_data(stock_id)
    parse_sine_static_stock_content(main_content, stk)
    return stk

def dump_stock_header_to_string(stk):
    return ",".join([i for i in stk.keys()])

def dump_stock_to_string(stk):
    return ",".join([i for i in stk.values()])

def start(stock_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = "{}/stock_{}".format(output_dir.rstrip('/'), date.today().strftime("%Y%m%d"))
    with open(stock_file) as f, open(output_file, 'w', encoding="utf-8") as out:
        isFirst = True
        for line in f:
            first_char = line[0]
            stock_id = line.strip()
            if first_char.isnumeric():
                if first_char == 3 or first_char == 6:
                    stock_id = "sh" + stock_id
                if first_char == 0 or first_char == 1:
                    stock_id = "sz" + stock_id
                else:
                    continue
            retryTime = 0
            while retryTime < MAX_RETRY:
                try:
                    logger.info("crawl:" + stock_id)
                    stk = crawl_stock(stock_id)
                    if isFirst:
                        header = dump_stock_header_to_string(stk)
                        out.write(header + "\n")
                        isFirst = False
                    stock_dump = dump_stock_to_string(stk)
                    out.write(stock_dump + "\n")
                    logger.info(stock_dump)
                    time.sleep(10)
                    break
                except KeyboardInterrupt:
                    return
                except IndexError as e:
                    exc_type, exc_obj, tb = sys.exc_info()
                    logger.warning("cannot scrape for {}. index error:{}. linenum:{}".format(stock_id, str(e), tb.tb_lineno))
                    time.sleep(2)
                    break
                except Exception as e:
                    exc_type, exc_obj, tb = sys.exc_info()
                    logger.warning("cannot scrape for {}. exception:{}. linenum:{}".format(stock_id, str(e), tb.tb_lineno))
                    time.sleep(3)
                    retryTime += 1
        
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", help="input file", default=INPUT_FILE)
parser.add_argument("-o", "--output_dir", help="output dir", default=OUTPUT_DIR)
#parser.add_argument("-l", "--log_file", help="log file path", default=LOG)

if __name__ == '__main__':
    args = parser.parse_args()
    INPUT_FILE = args.input_file
    OUTPUT_DIR = args.output_dir
#    LOG = args.log_file
    start(INPUT_FILE, OUTPUT_DIR)
    