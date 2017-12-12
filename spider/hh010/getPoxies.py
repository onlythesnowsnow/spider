#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib
from urllib import urlencode
 
#----------------------------------
# 实时IP代理库调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/62
#----------------------------------
 
def main():
 
    #配置您申请的APPKey
    appkey = "*********************"
 
    #1.获取免费代理
    request1(appkey,"GET")
 
 
 
#获取免费代理
def request1(appkey, m="GET"):
    url = "http://japi.juheapi.com/japi/fatch"
    params = {
        "v" : "", #版本，当前1.0
        "pkg" : "", #包名，没有则留空
        "key" : appkey, #应用APPKEY(应用详细页查询)
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
    else:
        print "request api error"
 
 
 
if __name__ == '__main__':
    main()
