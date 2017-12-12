#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import requests
from bs4 import BeautifulSoup
import urllib2
import urllib
print sys.getdefaultencoding()
import time as tt
import re
import pymongo
import threading
import Queue
import os
import datetime


headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'_uab_collina=147021548421953380060196; ki1e_2132_pc_size_c=0; ki1e_2132_saltkey=OJ5q3jCt; ki1e_2132_lastvisit=1474090123; ki1e_2132_sendmail=1; _umdata=0712F33290AB8A6D93ED2B0B8208412BC0748B7EF9CC5D8A6129B492436AB5BDE5570C69A970F5D68381D35217FF8174BF5E135F2B5FA1D57B5A3D6F518F68746B40D817712CB479C0A87EACA6376DB46AF39B339057F19778485D2A13019E0B; ki1e_2132_ulastactivity=1474093831%7C0; ki1e_2132_auth=0b41J27j4t7Pn8JVVN5SN2exTDEt95sraX4C4M0BOfqfynUrkIzEHTRv5JTdrTQtvJxD7zrmuxINFOmJRwKUhOEvRdQ; tjpctrl=1474095635029; ki1e_2132_home_diymode=1; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1473408853,1473815191,1474080612,1474093673; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1474093866; AJSTAT_ok_pages=19; AJSTAT_ok_times=10; amvid=120a52dd7f69e50392c402831d875196; ki1e_2132_lastact=1474093986%09forum.php%09ajax; ki1e_2132_connect_is_bind=0',
'Host':'www.zuanke8.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}


url = 'http://www.zuanke8.com/home.php?mod=space&uid='
uid_start = '280000'
uid_end = '480000'
netname = 'zuanke8_info'
#548004
#438840
#308619
#1378990

client = pymongo.MongoClient(host="172.29.152.230", port=27017)
client.admin.authenticate("nslab", "nslab")
db = client['spider']
    # 在此处更改为你自己的网站名称！
collection = db[netname]
def get_page(viewHref, number):
	UserName = ''
	UID = ''
	HomePage = ''
	RegistrationData = ''
	DateLastAccessed = ''
	DataLastActivity = ''
	DataLastPosted = ''
	NumSpaceVisited = ''
	NumFriends = ''
	NumReply = ''
	NumPosts = ''
	MemberPoints = ''
	Prestige = ''
	LevelAdministrator = ''
	LevelUserGroup = ''
 	try:
		html = requests.get(viewHref,headers=headers).content
	except:
		return 1
	soup = BeautifulSoup(html,'lxml',from_encoding="utf-8")
	#print soup
#	UserName = str(soup.findAll(attrs={'class': 'bm_c'})[0].get_text()).split(' (UI')[0]
#	print UserName
	UID = str(number)
	print UID
	HomePage = viewHref
	print HomePage

	try:
		lists1 = soup.findAll(attrs={'class': 'mbn'})[1]
		UserName = lists1.contents[0].strip('\r\n')
		print UserName
	except:
		return 2
	kongjian = soup.findAll('em')
	try:
		#for i in kongjian:
		#	if i.get_text() =="空间访问量":
		#		print i.next_sibling.get_text()
		#		NumSpaceVisited = i.next_sibling.get_text()


		lists2 = soup.find(attrs={'id': 'pbbs'})
		for i in lists2:
			if str(type(i)) != "<class 'bs4.element.NavigableString'>":
				if i.em.get_text() == "注册时间":
					print i.contents[1]
					RegistrationData = i.contents[1]
				if i.em.get_text() == "最后访问":
					print i.contents[1]
					DateLastAccessed = i.contents[1]
				if i.em.get_text() == "上次活动时间":
					print i.contents[1]
					DataLastActivity = i.contents[1]
				if i.em.get_text() == "上次发表时间":
					print i.contents[1]
					DataLastPosted = i.contents[1]

		lists4 = soup.findAll(attrs={'class': 'pf_l'})[-1]
		for i in lists4:
			if str(type(i)) != "<class 'bs4.element.NavigableString'>":
				if i.em.get_text() == "积分":
					print i.contents[1]
					MemberPoints = i.contents[1]

		NumFriends = re.findall('好友数[\d\s:]+', str(soup))
		NumFriends = NumFriends[0].split(' ')[1]
		print NumFriends
		NumReply = re.findall('回帖数[\d\s:]+', str(soup))
		NumReply = NumReply[0].split(' ')[1]
		print NumReply
		NumPosts = re.findall('主题数[\d\s:]+', str(soup))
		NumPosts = NumPosts[0].split(' ')[1]
		print NumPosts
	
		lists3 = soup.findAll(attrs={'class': 'xg1'})[-1]
		LevelUserGroup = lists3.next_sibling.a.get_text()
		print LevelUserGroup
	except:
		pass

	tt.sleep(0.1)

	symbol_dict = {
	'UserName': UserName,
	'UID': UID,
	'HomePage': HomePage,
	'RegistrationData': RegistrationData,
	'DateLastAccessed': DateLastAccessed,
	'DataLastActivity': DataLastActivity,
	'DataLastPosted': DataLastPosted,
	'NumSpaceVisited': NumSpaceVisited,
	'NumFriends': NumFriends,
	'NumReply': NumReply,
	'NumPosts': NumPosts,
	'MemberPoints': MemberPoints,
	'Prestige': Prestige,
	'LevelAdministrator': LevelAdministrator,
	'LevelUserGroup': LevelUserGroup
	} 
	
	collection.insert(symbol_dict)
	return 3


class LookUp(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		
	def run(self):
		global queue_viewHref, mutex_href_get, mutex_href_put
		mutex_href_get.acquire()
		while queue_viewHref.qsize() > 0:
			# 在线程池中取得链接和序号
			viewHref_and_number = queue_viewHref.get()
			viewHref = str(viewHref_and_number.split("wxw")[0])
			number = str(viewHref_and_number.split("wxw")[1])
			mutex_href_get.release()
			viewHref = viewHref + '&do=profile'
			# 调用get_page函数
			result = get_page(viewHref, number)
			print '1111111111111111111111111111111111111122222222222222'
			print  result
			print '111'*10
			try:
				mutex_href_put.acquire()
				if result ==1:
					pass
				elif result ==2:
					pass
				elif result ==3:
					pass
				else:
					logUnExpected(viewHref)
				mutex_href_put.release()
			except:
				mutex_href_put.release()
				mutex_href_get.acquire()
				continue
			mutex_href_get.acquire()
		mutex_href_get.release()



def get_all():

    global queue_viewHref, mutex_href_get, mutex_href_put
    queue_viewHref = Queue.Queue()  # 任务队列，每一项为帖子的url 
    threads = []
    # 线程数量
    num = 32
    mutex_href_get = threading.Lock()
    mutex_href_put = threading.Lock()
    for k in xrange(int(uid_start), int(uid_end)):
        viewHref = url + str(k) 
	# 把链接和序号同时放入队列，用"wxw"隔开
	queue_viewHref.put(viewHref+"wxw"+str(k))

    for i in xrange(0, num):
	threads.append(LookUp())

    for thread in threads:
	thread.start()

    for thread in threads:
	thread.join()






get_all()




