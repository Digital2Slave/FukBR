#-*- coding:utf-8 -*-
"""
Name    : main
Author  : JohnTian
Date    : 12/18/2015
Version : 0.01
CopyLeft: OpenSource
"""
from config      import *
from bookcover   import parse
from bookhelper  import AmazonIsbn2Asin

import time
import json
import pymongo
from pymongo  import MongoClient
from optparse import OptionParser
from multiprocessing import Pool

def help():
    print  '''
            Usage :
            $ python <name>.py --input=<isbnspath> --pool=<corenumber>
            eg:
            $ python main.py --input='./file/data/isbns_i.json' --pool=4
        '''

def isbn2bookdata(isbn):
    asin  = AmazonIsbn2Asin(isbn)
    if (asin != ''):
        bookdict = parse(isbn, asin)
        item     = {}
        item['bookinfo'] = bookdict
        return item

def bookdata2mongoData(item):
    if item != None:
        # !< connect mongodb
        client    = MongoClient(host=MONGODB_SERVER, port=MONGODB_PORT)
        db        = client[MONGODB_DB]
        bookcover = db[MONGODB_COLLECTION]
        bookcover.update({'bookinfo':item['bookinfo']}, item, upsert=True)

def run(data, cores=4):
    pool = Pool(cores)
    items = pool.map(isbn2bookdata, data)
    pool.close()
    pool.join()

    pool = Pool(cores)
    pool.map(bookdata2mongoData, items)
    pool.close()
    pool.join()


def test(data):
    # spark given number of processes
    print 'start......'
    pool = Pool(4)
    t1 = time.time()
	# map to pool
    items = pool.map(isbn2bookdata, data)
    pool.close()
    pool.join()
    t2 = time.time()
    print t2-t1
    print 'bookdata done...'

    pool = Pool(4)
    pool.map(bookdata2mongoData, items)
    pool.close()
    pool.join()
    t3 = time.time()
    print t3-t2
    print 'mongodata done...'

if (__name__=='__main__'):
    try:
        parser = OptionParser()
        parser.add_option("-f", "--input", action="store", dest="isbnData", help="Load isbn file.")
        parser.add_option("-i", "--pool", action="store", dest="cores", help="Set pool number.")
        (options,args) = parser.parse_args()
        filename       = options.isbnData
        cores          = options.cores
    except:
        help()

    # !< load data
    with open(filename, 'rb') as fi:
        data = json.load(fi)
    fi.close()

    # !< split data
    step = 100
    splitdatas = [data[i:i+step] for i in xrange(0,len(data),step)]

    # !< handle each
    for d in splitdatas:
        run(d, cores)
        time.sleep(3)
