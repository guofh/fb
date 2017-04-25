#coding=utf-8


import sys
import browser
import proxy
import threading
import time
import datetime
import random

reload(sys)
sys.setdefaultencoding("utf-8")

class auto_brush():

    p = proxy.proxy();

    urls=['https://www.woquba.cn','https://www.baidu.com','http://www.ip138.com']
    url_weight=[]

    ips=[]

    threads=[]
    thread_num = 10

    time_distribution=[2,1,1,2,3,4,5,6,7,7,7,8,9,7,6,5,5,7,8,9,9,8,7,5]
    total_fb = sum(time_distribution)
    base_num = 10000

    last_hour = 0;
    last_min = 0;
    rand = random.randint(-10,10)
    last_task_num = int((base_num/total_fb)*(time_distribution[last_hour]+rand/10.0))

    residue_sec = 3600
    residue_task = last_task_num*len(urls)

    #########################################################################
    #
    #                   自动刷量主程序
    #
    #########################################################################
    def run(self):
        self.__init_url_weight__()
        self.__update_ips__()


        while True:
            self.__update_task__()
            if len(self.ips)<=0 :
                self.__update_ips__()

            if len(self.threads) < self.residue_task:
                self.__add_thread_task__()
                self.residue_task = self.residue_task-1
                print "add thread task,residue task is",self.residue_task

            if self.residue_sec >= self.residue_task:
                st = self.residue_sec/self.residue_task
                print "sleep time is",st,"residue_sec is ",self.residue_sec
                time.sleep(st)
                self.residue_sec = self.residue_sec-st
    #########################################################################
    #
    #                   更新任务列表和代理ip列表{}
    #
    #########################################################################
    def __update_task__(self):
            now = datetime.datetime.now()
            hour = now.hour
            minite = now.minute

            if hour is not self.last_hour:
                self.rand = random.randint(-10,10)
                self.last_task_num = int((self.base_num/self.total_fb)*(self.time_distribution[hour]+self.rand/10.0))
                self.last_hour = hour
                self.residue_sec = 3600
                self.residue_task = self.last_task_num*len(self.urls)
                print self.rand,self.last_task_num

            if ((minite - self.last_min)>5) | (hour is not self.last_hour):
                self.__update_ips__()
                self.last_min = minite


    #########################################################################
    #
    #                   添加一个线程
    #
    #########################################################################
    def __add_thread_task__(self):
        for t in self.threads:
            if not t.isAlive():
                self.threads.remove(t)
                #print "thread release,thread num ",t

        if len(self.threads)<self.thread_num:
            index = self.__get_url_index__()
            t = threading.Thread(target=self.__task__,args=(index,))
            self.threads.append(t)
            #t.setDaemon(True)
            t.start()


    #########################################################################
    #
    #                   线程处理函数
    #
    #########################################################################
    def __task__(self,index):
        b = browser.SeleniumBrowser()
        self.url_weight[index] = self.url_weight[index]+1

        ht = 'http'
        ip = '117.90.1.128'
        port = '9000'

        #b.open_url_proxy(self.urls[index],ht,ip,port)
        b.open_url(self.urls[index])
        self.url_weight[index] = self.url_weight[index]-1
        #print "thread start,thread num is",len(self.threads),index



    #########################################################################
    #
    #                   初始化网站列表中的各网站任务分布
    #
    #########################################################################
    def __init_url_weight__(self):
        for i in range(len(self.urls)):
           # self.url_weight[i]=0
           self.url_weight.append(0)



    #########################################################################
    #
    #                   更新任务列表和代理ip列表{}
    #
    #########################################################################
    def __update_ips__(self):
        self.ips = self.p.get_proxy_ips()


    #########################################################################
    #
    #           根据网站任务分布情况选择一个处理量最低的网站索引
    #
    #########################################################################
    def __get_url_index__(self):
        minNum = self.url_weight[0]
        index = 0
        for i in range(len(self.url_weight)):
            if minNum > self.url_weight[i]:
                minNum = self.url_weight[i]
                index = i

        print self.url_weight,'website is',self.urls[index],'weight is',minNum
        return index





test = auto_brush()
test.run()





