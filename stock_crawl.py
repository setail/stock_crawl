#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 21:56:27 2017

@author: frank
"""

import time
import argparse
from datetime import date

import sys
import os
import shutil
import random
import traceback
from urllib.error import HTTPError
from collections import OrderedDict

import sina_stock_crawler
import globl
from globl import stock_cols

LOG = "./log"
OUTPUT_DIR = "./data"
INPUT_FILE = "./data/all_stock_ids"
MAX_RETRY = 3
logger = globl.get_logger()

def dump_stock_header_to_string(stk):
    return ",".join([i for i in stk.keys()])

def dump_stock_to_string(stk):
    return ",".join([i for i in stk.values()])

def start(stock_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = "{}/stock_{}".format(output_dir.rstrip('/'), date.today().strftime("%Y%m%d"))
    file_name = output_file
    if os.path.exists(file_name):
        file_name = "{}.{}.bak".format(file_name, time.strftime('%l_%M%p'))
        shutil.move(output_file, file_name)
    crawler = sina_stock_crawler
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
                    stk = OrderedDict()
                    stk[stock_cols.ID] = stock_id
                    crawler.crawl_stock_data(stk, stock_id)
                    if isFirst:
                        header = dump_stock_header_to_string(stk)
                        out.write(header + "\n")
                        isFirst = False
                    stock_dump = dump_stock_to_string(stk)
                    out.write(stock_dump + "\n")
                    logger.info(stock_dump)
                    time.sleep(random.randrange(3, 10))
                    break
                except KeyboardInterrupt:
                    return
                except (IndexError, HTTPError) as e:
                    exc_type, exc_obj, tb = sys.exc_info()
                    logger.warning("cannot scrape for {}. index error:{}. linenum:{}".format(stock_id, str(e), tb.tb_lineno))
                    time.sleep(2 * 1<<retryTime)
                    break
                except Exception as e:
                    exc_type, exc_obj, tb = sys.exc_info()
                    logger.warning("cannot scrape for {}. exception:{}. linenum:{}".format(stock_id, str(e), tb.tb_lineno))
                    traceback.print_tb(e.__traceback__)
                    time.sleep(random.randrange(3, 10))
                    break
        
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", help="input file", default=INPUT_FILE)
parser.add_argument("-o", "--output_dir", help="output dir", default=OUTPUT_DIR)
#parser.add_argument("-l", "--log_file", help="log file path", default=LOG)

if __name__ == '__main__':
    args = parser.parse_args()
    INPUT_FILE = args.input_file
    OUTPUT_DIR = args.output_dir
    start(INPUT_FILE, OUTPUT_DIR)
    