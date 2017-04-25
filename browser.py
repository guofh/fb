#coding=utf-8

import mechanize
import sys
import cookielib
import time
import random


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

reload(sys)
sys.setdefaultencoding("utf-8")

ER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",

]

class MechanizeBrowser():

    br = mechanize.Browser()

    def init_browser(self):
        #options
        #cj = cookielib.LWPCookieJar()
        #self.br.set_cookiejar(cj)
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)

        #Follows refresh 0 but not hangs on refresh > 0
        #self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=30)

        #debugging?
        #self.br.set_debug_http(True)
        #self.br.set_debug_redirects(True)
        #self.br.set_debug_responses(True)

        #User-Agent (this is cheating, ok?)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    def open_url(self,url):

        r = self.br.open(url)
        print r.read()
        #print r.geturl()
        #print self.br.response().read()
        #print self.br.title()
        #print r.info()

    def open_url_proxy(self,url,ht,proUrl,port):

        self.br.set_proxies({ht:proUrl+':'+port})
        try:
            self.open_url(url)
        except Exception,e:
            print "browser open url with proxy error!",e




class SeleniumBrowser():

    main_page = ''
    #########################################################################
    #
    #                   初始化浏览器
    #
    #########################################################################
    def __init_browser__(self,proxyFlag=None,ht=None,proUrl=None,port=None):
        if proxyFlag is True:
            ht = unicode(ht)
            proUrl = unicode(proUrl)
            port = unicode(port)
            proxy = proUrl+':'+port

            #dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap = DesiredCapabilities.PHANTOMJS.copy()
            dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0")
            #dcap["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENTS))
            dcap["phantomjs.page.settings.resourceTimeout"] = ("1000")
            #dcap = DesiredCapabilities.PHANTOMJS.copy()
            #从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
            #dcap["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENTS))
            # 不载入图片，爬页面速度会快很多
            #dcap["phantomjs.page.settings.loadImages"] = False
            # 设置代理
            #service_args = ['--proxy='+proUrl+':'+port,'--proxy-type=socks5']
            s_args = ['--web-security=no','--ignore-ssl-errors=yes','--ssl-protocol=any']
            #s_args = ['--web-security=no','--ignore-ssl-errors=true', '--ssl-protocol=any','--proxy='+proUrl+':'+port,'--proxy-type='+ht]
            #s_args = ['--ignore-ssl-errors=true', '--ssl-protocol=any','--proxy='+proUrl+':'+port,'--proxy-type='+ht,'--proxy-auth=username:password']
            #service_args = ['--proxy='+proUrl+':'+port]
            #print s_args
            #打开带配置信息的phantomJS浏览器
            #self.browser1 = webdriver.PhantomJS(desired_capabilities=dcap,service_args=s_args)
            #self.browser1 = webdriver.PhantomJS(service_args=s_args)

            dcap['proxy'] = {'proxyType':'MANUAL','httpProxy': proxy,'ftpProxy': proxy,'sslProxy': proxy,'noProxy': None}
            dcap["acceptSslCerts"] = True
            dcap['phantomjs.cli.args'] = ['--web-security=false','--ignore-ssl-errors=true','--ssl-protocol=any']
            #dcap['proxy'] = {'httpProxy': proxy,'ftpProxy': proxy,'sslProxy': proxy,'noProxy': None}
            #chrome_options = webdriver.ChromeOptions()
            #chrome_options.add_argument("ignore-certificate-errors=true")
            #chrome_options.add_argument("--web-security=false")
            #chrome_options.add_argument("--ssl-protocol=any")
            #chrome_options.add_argument('--proxy-server='+ht+'://'+proUrl+':'+port)
            #browser = webdriver.Chrome(chrome_options=chrome_options)

            browser = webdriver.PhantomJS(desired_capabilities=dcap,service_args=s_args)
            #self.browser1 = webdriver.PhantomJS(desired_capabilities=dcap)
            #self.browser1.capabilities["acceptSslCerts"] = True
            #self.browser1.capabilities["proxy"] = {u"proxy": proUrl+':'+port,u"proxy-type":ht}
            #self.browser1.capabilities["proxy"] = {u"proxyType":u"MANUAL",u"httpProxy": proUrl+':'+port}
            #self.browser1.capabilities['proxy'] = {'proxyType': 'MANUAL','httpProxy': proxy,'ftpProxy': proxy,'sslProxy': proxy,'noProxy': None}

            #self.browser1.capabilities["proxy"] = ht+"://"+proUrl+':'+port

            #profile = webdriver.FirefoxProfile()
            #profile.set_preference('network.proxy.type', 1)
            #profile.set_preference('network.proxy.http', proUrl)
            #profile.set_preference('network.proxy.http_port', port)
            #profile.set_preference('network.proxy.ssl', proUrl)
            #profile.set_preference('network.proxy.ssl_port', port)
            #profile.update_preferences()
            #browser = webdriver.Firefox(profile)

        else:
            #browser = webdriver.Firefox()
            #browser = webdriver.Firefox(service_args=['--ignore-ssl-errors=true'])
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("ignore-certificate-errors");
            browser = webdriver.Chrome(chrome_options=chrome_options)



        # 隐式等待5秒，可以自己调节
        browser.implicitly_wait(30)
        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        browser.set_page_load_timeout(30)
        # 设置10秒脚本超时时间
        browser.set_script_timeout(30)
        print browser.capabilities

        browser.maximize_window()

        return browser
        #self.browser.set_window_size(480,800)

    #########################################################################
    #
    #                   关闭浏览器
    #
    #########################################################################
    def __close_browser__(self,br):
        try:
            #br.close()
            br.quit()
        except Exception,e:
            print "close browser,",e

    #########################################################################
    #
    #                   自动浏览函数，包括浏览深度，浏览时间等
    #
    #########################################################################
    def __auto_browse__(self,browser):

        minBrowseTime = 10
        maxBrowseTime = 60
        minBrowseNum = 1
        maxBrowseNum  = 5

        totalSleepTime = random.randint(minBrowseTime,maxBrowseTime)
        totalBrowseNum = random.randint(minBrowseNum,maxBrowseNum)

        residueTime = totalSleepTime
        residueBrowseNum = totalBrowseNum

        cur_url = self.main_page

        try:
            browser.get(self.main_page);
            time.sleep(random.randint(1,15))
            print browser.page_source
        except Exception,e:
            #self.__close_browser__(browser)
            print "browser open url error!",e

        #for link in all_links:
            #if not '_blank' in link.get_attribute("target") and
            #print link.get_attribute("href")

        print 'total sleep time is',totalSleepTime,',total browse num is',totalBrowseNum

        while ((residueBrowseNum - 1) >= 0):

            if residueTime <=0:
                break

            residueBrowseNum-=1
            if residueTime - residueBrowseNum>1:
                curSleepTime = random.randint(1,(residueTime-residueBrowseNum))
            else:
                curSleepTime = residueTime
            residueTime-=curSleepTime

            print 'curSleepTime is',curSleepTime,',residueTime is',residueTime,',residueBrowseNum is',residueBrowseNum,',cur browser url is',cur_url

            try:

                all_links = browser.find_elements_by_tag_name('a')
                link = random.sample(all_links,1)
                if link:
                    cur_url = link[0].get_attribute("href")
                    link[0].click()
                else:
                    cur_url = self.main_page
                    browser.get(self.main_page);

                time.sleep(curSleepTime)

                #browser.back()

                #print browser.page_source
            except Exception,e:
                #self.__close_browser__(browser)
                print "browser error!",e

        self.__close_browser__(browser)



    #########################################################################
    #
    #                  普通方式打开代理
    #
    #########################################################################
    def open_url(self,url):

        self.main_page = url
        browser = self.__init_browser__()
        self.__auto_browse__(browser)

    #########################################################################
    #
    #                   使用代理打开网站
    #
    #########################################################################
    def open_url_proxy(self,url,ht,proUrl,port):

        self.main_page = url
        browser = self.__init_browser__(True,ht,proUrl,port)
        self.__auto_browse__(browser)

    #########################################################################
    #
    #                   测试（使用代理打开网站）
    #
    #########################################################################
    def open_url_proxy1(self,url,ht,proUrl,port):

        br = webdriver.PhantomJS()
        br.get(url)
        print br.page_source
        print br.capabilities

        proxy = webdriver.Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = proUrl+':'+port
        proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
        br.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
        br.get(url)
        print br.page_source
        print br.capabilities


#########################################################################
#
#                   测试程序
#
#########################################################################
if __name__ == "__main__":

    ht = 'http'
    ip = '59.48.65.11'
    port = '8000'

    #url = 'http://1212.ip138.com/ic.asp'
    #url = 'https://www.baidu.com'
    url = 'http://icanhazip.com/'
    #url = 'https://www.woquba.cn'
    #url = 'http://ip.chinaz.com'
    #url = 'http://www.liuxiangchugui.com'

    ab = SeleniumBrowser()
    #ab.open_url(url)
    ab.open_url_proxy(url,ht,ip,port)

    #tt = MechanizeBrowser()
    #tt.init_browser()
    #tt.open_url_proxy(url,ht,ip,port)
    #tt.open_url(url)

