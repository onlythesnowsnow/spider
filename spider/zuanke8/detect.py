#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import requests
from bs4 import BeautifulSoup
from crawlspider import *
import urllib2
import urllib
from user_agent import *
print sys.getdefaultencoding()
import time as tt

'''
----------------------相关全局变量---------------------
'''

# 网站url的英文名称，是mongo数据库的表名
netname = 'zuanke8'
# 序号越小，则时间越早 只要找到最早或者较早的帖子序号，以及6月30日之前的帖子序号就可以
start_page_number = 4160771
end_page_number = 4479429
#25219
#                  13071450
#代理服务器IP  如果被封了就换一个
#proxies = {"http": "http://202.100.167.144:80"}

Url = 'http://www.zuanke8.com/'

'''
----------------------相关用户信息-----------------------
'''
#以下不同的帐号不一样，需要修改
#建议多开小号 在封禁之前迅速爬
#################################################
cookie = {'ki1e_2132_saltkey=k7tfF7nf; ki1e_2132_lastvisit=1510664258; ki1e_2132_lastact=1510667874%09connect.php%09check; ki1e_2132_sendmail=1; _uab_collina=151066775090869890875046; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1510667754; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1510667766; ki1e_2132_pc_size_c=0; ki1e_2132_atarget=1; ki1e_2132_forum_lastvisit=D_13_1510667868; amvid=7e00cbd6f30746676269ee0e9ed85f1e; ki1e_2132_viewid=tid_4476536'}


headers = { 
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'ki1e_2132_saltkey=k7tfF7nf; ki1e_2132_lastvisit=1510664258; ki1e_2132_lastact=1510667874%09connect.php%09check; ki1e_2132_sendmail=1; _uab_collina=151066775090869890875046; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1510667754; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1510667766; ki1e_2132_pc_size_c=0; ki1e_2132_atarget=1; ki1e_2132_forum_lastvisit=D_13_1510667868; amvid=7e00cbd6f30746676269ee0e9ed85f1e; ki1e_2132_viewid=tid_4476536',
'Referer':'http://www.zuanke8.com/forum-2-1.html',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'

}


if __name__ == '__main__':
    """
    @ date: 2016-7-23
    @ function: 整个爬虫的接口函数。
                1.调用crawlspider，爬取论坛的主贴及回帖
                2.调用crawlspider，对可能因网络原因造成的失败url进行重新爬取。
                3.调用click，对需要论坛币支付才可见的帖子进行爬取。
                同时在每次爬取时，以文件形式分别记录成功及失败的帖子，以备后用
    @ input: 	1,输入网址/开始序号/结束序号/数据库名称/代理IP的全局变量
                2,输入登陆网站的用户信息
    @ output: 	1.输出文件error1.txt记录第一次爬取时未能爬取成功的帖子所在版块及url。
                2.输出文件error2.txt记录第二次爬取，即爬取error1时未能爬取成功的帖子所在版块及url。
                3.输出文件error3.txt记录了第三次爬取，即爬取error2时未能爬取成功的帖子所在版块及url。
                4.输出文件 $版块.txt 记录了爬取成功的帖子内容等信息
                5.输出到远程mongodb上爬取成功的帖子内容等信息
                6.输出文件error_form记录了由于帖子格式问题爬取失败的链接
                7.输出文件page_not_exist.txt记录了该序号的帖子不存在的链接
                8.输出文件need_buy.txt记录了需要购买的帖子的链接
    @ warning:  先在本地进行实验，若能成功运行则爬取

   
    """

    print 1111

    # 爬取所填写的所有版块的帖子
    # 生成$版块.txt error1.txt 导入mongodb
    grade = 1
    # 以下是该模块的链接
    # 不同的网站格式不同
    spiderUrl = Url + 'thread-'
    get_all(spiderUrl, grade)

    print "输入的序号范围内所有帖子爬取结束！"




    # 读取因网络等问题未能爬取成功的帖子所在的error1文件
    # 进行再次爬取
    #with open('error1.txt', 'r') as f1:
    #    # error的等级
    #    grade = 2
    #    for i in f1.readlines():
    #        number = number + 1
    #        viewHref = str(i)
    #	    number = int(viewHref.split('r')[1])
    #        crawlspider.get_all(viewHref, grade, number)
    #        print "现在验证到"+str(number)+"!"

    # 如需此功能，可解除注释
    # 对经过一次验证后仍然错误的帖子进行爬取，可能是因为需要支付金币后可见，所以调用selenium库进行模拟鼠标点击支付
    # 若还是不能爬取成功，记录到error3文件
    #with open('error2.txt', 'a') as f2:
    #    # error的等级
    #    grade = 3
    #    # 该贴所在的页数或位序
    #    number = 0
    #    for i in f2.readlines():
    #        number = number + 1
    #        board = str(i.split(' ')[0])
    #        get_fid = str(i.split(' ')[1])
    #       viewHref = str(i.split(' ')[2])
    #        click_to_pay(viewHref, grade, board, get_fid)
    #        crawlspider.get_all(board, get_fid, viewHref, grade, number)
    #        print "现在验证到第" + str(number) + "个!"

    print "三次爬取完成，若error3及error_form,error_page中存在帖子，请人工检查那些网页！"










