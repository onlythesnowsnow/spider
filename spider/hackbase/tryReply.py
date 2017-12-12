#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from bs4 import BeautifulSoup
import time as tt
import requests
from detect import *
from crawlspider import *
from store import *
from user_agent import *


def send_post(grade, number, viewHref):
    # 构造Post请求链接
    postHref = Url + 'forum.php?mod=post&action=reply' + '&tid=' + str(
        number) + '&extra=&replysubmit=yes&mobile=yes'
    # 先发送一个Post来回帖 再爬取内容
    # 若发送了post请求 但回复失败 记录错误
    try:
        check_if_right = requests.post(postHref, cookies=cookie, headers=headers, data=post_data, timeout=70).content
        # 这里由不同网站回帖的间隔最小时间来决定
	tt.sleep(60)
        check_if_right_soup = BeautifulSoup(check_if_right, 'lxml', from_encoding="utf-8")
	print check_if_right_soup
    except:
        logErrorGrade(grade, viewHref)
        return False



