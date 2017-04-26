#coding=utf-8


import sys
import browser


reload(sys)
sys.setdefaultencoding("utf-8")

class proxy():

    dailis=['kuaidaili']

    def get_proxy_ips(self):
        return self.kuaidaili()

    def kuaidaili(self):
        dailiUrl = 'http://dev.kuaidaili.com/api/getproxy/?orderid=979313029617371&num=500&b_pcchrome=1&b_pcie=1&b_pcff=1&carrier=2&protocol=0&method=1&an_ha=1&sp1=1&sep=2'
        br = browser.MechanizeBrowser()
        br.init_browser()
        response = br.open_url(dailiUrl)
        context = response.read()
        ips_arr = context.split('\n')

        return ips_arr

#########################################################################
#
#                   测试程序
#
#########################################################################
if __name__ == "__main__":

    pro = proxy()
