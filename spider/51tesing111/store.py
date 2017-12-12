#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import json
import pymongo

class storeContent():

    def store_in_file(self, symbol_dict, board):
        file_object = open(str(board)+"2323" +'.txt', 'a')
        symbol_dict = json.dumps(symbol_dict, encoding="UTF-8", ensure_ascii=False, indent=4)
        file_object.write(str(symbol_dict).encode('utf-8'))
        file_object.close()
    def store_in_remote_mongodb(self, symbol_dict, netname):
        client = pymongo.MongoClient(host="172.29.152.153", port=27017)
        client.admin.authenticate("root", "hitnslab")
        db = client['spider']
        # 在此处更改为你自己的网站名称！
        collection = db[netname]
        collection.insert(symbol_dict)
    def store_viewHref(self, viewHref):
	with open('completed_url.txt','a') as f:
		f.write(viewHref+"\n")

def logErrorGrade(grade, viewHref):
    with open('error' + str(grade) + '.txt', 'a') as f:
        f.write(str(viewHref))
        f.write('\n')

def logErrorForm(viewHref):
    with open('error_form.txt', 'a') as f:
        f.write(str(viewHref))
        f.write('\n')

def logNotExistPage(viewHref):
    with open('page_not_exist.txt','a') as f:
	f.write(viewHref+"\n")
    print 'this page does not exist'

def logUnExpected(viewHref):
    with open('UnExpected.txt','a') as f:
	f.write(viewHref + "\n")

def logNeedClick(viewHref):
    with open('need_click.txt','a') as f:
	f.write(viewHref +"\n")

def logNeedBuy(viewHref):
    with open('need_buy.txt','a') as f:
	f.write(viewHref + "\n")



