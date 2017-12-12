#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from bs4 import BeautifulSoup
import urllib2
import urllib
import re
import codecs
import time as tt
import demjson
import json
import requests
import pymongo
from store import *
import tryReply
from detect import *
from lxml import etree  
import threading
import Queue
import os
import datetime



#用于匹配日期的正则表达式
compiled_time=re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')
compiled_time2=re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+')

class LookUp(threading.Thread):
	def __init__(self, grade):
		threading.Thread.__init__(self)
		self.grade = grade

	def run(self):
		global queue_viewHref, mutex_href_get, mutex_href_put
		mutex_href_get.acquire()
		while queue_viewHref.qsize() > 0:
			# 在线程池中取得链接和序号
			viewHref_and_number = queue_viewHref.get()
			viewHref = str(viewHref_and_number.split("wxw")[0])
			number = str(viewHref_and_number.split("wxw")[1])
			mutex_href_get.release()

			# 调用get_page函数
			result = get_page(viewHref, self.grade, number)
			print '1111111111111111111111111111111111111122222222222222'
			print  result
			print '111'*10
			try:
				mutex_href_put.acquire()
				if str(type(result)) == "<type 'dict'>":
					self.board = str(result['1']['board'])
					print self.board
					print 22222222222222222222222222222222222222222222222222222222222222222	
    					storeIn = storeContent()
    					#storeContent.store_in_file(storeIn, result, self.board)
    					storeContent.store_in_remote_mongodb(storeIn, result, netname)
					storeContent.store_viewHref(storeIn, viewHref)
				elif result ==1:
					logErrorGrade(self.grade, viewHref)
				elif result ==2:
					logNotExistPage(viewHref)
				elif result ==3:
					logErrorForm(viewHref)
				elif result ==4:
					logNeedClick(viewHref)
				elif result ==5:
					logNeedBuy(viewHref)
				else:
					logUnExpected(viewHref)
				mutex_href_put.release()
			except:
				mutex_href_put.release()
				mutex_href_get.acquire()
				continue
			mutex_href_get.acquire()
		mutex_href_get.release()


def get_all(spiderUrl, grade):
    '''
    @ date: 2016-07-24
    @ function:爬取单独的一个帖子，便于代码的复用
    @ input: 该帖子所在板块的名称，板块fid值，该帖链接，错误级别，该帖在板块的页码号
    @ output: json_dict 是一个大字典。Key为楼层号，value为该楼层各种信息的小字典
    '''
    # 定义链接队列/得到链接的锁/给予链接的锁为全局变量
    global queue_viewHref, mutex_href_get, mutex_href_put
    queue_viewHref = Queue.Queue()  # 任务队列，每一项为帖子的url 
    threads = []
    # 线程数量
    num = 12
    mutex_href_get = threading.Lock()
    mutex_href_put = threading.Lock()

    for k in range(int(start_page_number), int(end_page_number)):
        viewHref = spiderUrl + str(k) +"&mobile=1" 
	# 把链接和序号同时放入队列，用"wxw"隔开
	queue_viewHref.put(viewHref+"wxw"+str(k))

    for i in xrange(0, num):
	threads.append(LookUp(grade))

    for thread in threads:
	thread.start()

    for thread in threads:
	thread.join()
	




def get_page(viewHref, grade, number):
    '''
    @ date: 2016-07-24
    @ function:爬取单独的一个帖子，便于代码的复用
    @ input: 该帖子所在板块的名称，板块fid值，该帖链接，错误级别，该帖在板块的页码号
    @ output: json_dict 是一个大字典。Key为楼层号，value为该楼层各种信息的小字典
    '''
    
    floor = 0

    print 111111111
    print 'hehe'

    tt.sleep(1.5)
    try:
        response0 = requests.get(viewHref, timeout=10, headers = headers).content
    except:
        #logErrorGrade(grade, viewHref)
        return 1

    soup0 = BeautifulSoup(response0, 'lxml', from_encoding="utf-8")
    
    # 如果该帖没有这个标签，证明这个帖子已被删除
    if not soup0.findAll(attrs={'class': 'box'}):
	#logNotExist(viewHref)
        return 2
    else:
    # 如果有 就记录下版块名称
	try:
		board = soup0.findAll(attrs={'class': 'box'})[0].findAll('a')[1].get_text()
        	print 'the page belongs to '+str(board)
	except:
		return 2
    # 如果有需要点击/回复才能看的 把该网址记录到文件 并跳过 
    ##if soup0.findAll(attrs={'class': 'f12  quoteTips'}):
	#logNeedClick(viewHref)
#	print 'we have a need_click'
 #       return 4

    # posts和Post_time这个列表里含有该页所有楼层的作者/时间信息
    posts = soup0.findAll(attrs={'class': 'bm_c bm_c_bg'})
    # posts_contents这个列表里含有该页所有楼层的正文信息
    posts_contents = soup0.findAll(attrs={'class':'mes'})
    # posts_head这个列表里含有该帖子的标题信息
    posts_head = soup0.findAll(attrs={'class': 'bm_h'})

    try:
        real_title = posts_head[0].get_text()
	print real_title
    except:
        print "获取标题出错！链接如下"
        print viewHref
       # logErrorForm(viewHref)
        return 3
    # 每爬取一个帖子，初始化存储有json格式数据的列表
    json_list = []  


    print "********************************************************"

    # 以下循环将正文部分处理成一整个字符串形式
    i = 0
    for post,  post_contents in zip(posts,posts_contents):
        # 初始化字典，该字典存有一个楼的数据
        json_dict = {}
        try:
            author = post.div.a.get_text()
	    print author
            time = compiled_time.search(str(post)).group()
	    print time
	    #print author,time
        except:
            print "ERROR:获取作者、时间信息出错！"
	    floor = 0
           # logErrorForm(viewHref)
            return 3

        lines = post_contents.encode('utf-8')
        lines = re.sub('[?]', '', lines)
        lines = re.sub('<span style=["]display:none["]>[^>]+>', '', lines)
        lines = re.sub('<font class=["]jammer["]>[^>]+>', '', lines)
        lines = re.sub('<(.*?)>', '', lines)
        lines = lines.strip()

        floor = floor + 1

        json_dict['author'] = str(author).decode('utf-8').encode('utf-8')
        json_dict['time'] = str(time).decode('utf-8').encode('utf-8')
        json_dict['content'] = lines.decode('utf-8').encode('utf-8')
        json_dict['floor'] = str(floor)

        # i 标记是否为第一楼，即楼主所在的楼层
        if i == 0:
            i = i + 1
            json_dict['href'] = viewHref.decode('utf-8').encode('utf-8')
            json_dict['title'] = real_title.decode('utf-8').encode('utf-8')
            json_dict['board'] = board

            json_list.append(json_dict)
            json_dict = {}
        else:
            json_list.append(json_dict)
            json_dict = {}
        print lines
        print 'the number is '+str(number)


    #################################################################################################
    all_contents = soup0.encode('utf-8')
    page_number = re.search('共 (\d+) 页',str(all_contents))
    if page_number:
    	print page_number.group()
	int_page_number = page_number.group()
	int_page_number = int_page_number[3:]
	int_page_number = int_page_number[:-3]
	int_page_number = int_page_number.strip()
	print int_page_number
    	print 1111111111111111111111111111111111111111
    	print 1111111111111111111111111111111111111111
    	print 1111111111111111111111111111111111111111
    	print 1111111111111111111111111111111111111111

    # 如果找到了下一页的标志元素 就跟踪其链接，爬取
    if page_number:
	now_page = 1
        while True:
	    now_page = now_page + 1
	    next_page_href = viewHref
	    next_page_href = next_page_href + '&page=' + str(now_page) 
	    print next_page_href
	    tt.sleep(1.5)
            try:
                response3 = requests.get(next_page_href, timeout=10, headers=headers).content
            except:
		floor = 0
                return 1
    	        # posts这个列表里含有该页所有楼层的作者/时间信息
	    soup3 = BeautifulSoup(response3, 'lxml', from_encoding="utf-8")
    	    posts3 = soup3.findAll(attrs={'class': 'bm_c bm_c_bg'})
    	    # posts_contents这个列表里含有该页所有楼层的正文信息
    	    posts3_contents = soup3.findAll(attrs={'class':'mes'})
 
            print "********************************************************"

   	    for post, post_contents in zip(posts3, posts3_contents):
            # 初始化字典，该字典存有一个楼的数据
            	json_dict = {}
            	try:
                	author = post.div.a.get_text()
	        	print author
                	time = compiled_time.search(str(post)).group()
	        	print time

            	except:
            		print "ERROR:获取作者、时间信息出错！"
			floor = 0
			return 3

        	lines = post_contents.encode('utf-8')
        	lines = re.sub('[?]', '', lines)
        	lines = re.sub('<span style=["]display:none["]>[^>]+>', '', lines)
        	lines = re.sub('<font class=["]jammer["]>[^>]+>', '', lines)
        	lines = re.sub('<(.*?)>', '', lines)
        	lines = lines.strip()

        	floor = floor + 1

        	json_dict['author'] = str(author).decode('utf-8').encode('utf-8')
        	json_dict['time'] = str(time).decode('utf-8').encode('utf-8')
        	json_dict['content'] = lines.decode('utf-8').encode('utf-8')
        	json_dict['floor'] = str(floor)

            	json_list.append(json_dict)
            	json_dict = {}

  #      	print lines
        	print 'the number is '+str(number)

            print "_______++++++++++_________++++++++++________"
            if int(now_page) >= int(int_page_number) :
                floor = 0
                break
		
    else:
        floor = 0



    symbol_list = map(lambda x: (x.get('floor'), x), json_list)
    symbol_dict = dict(symbol_list)
    print type(symbol_dict)
    return symbol_dict

    

