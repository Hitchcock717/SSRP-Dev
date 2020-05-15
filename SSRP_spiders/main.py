# -*- coding: utf-8 -*-
'''
    SSRP演示平台之爬虫运行主函数
'''

from SSRP_CNKIspider import CnkispaceSpider
from SSRP_CQVIPspider import CqvipSpider
from SSRP_WFspider import WFdataspider

from threading import Thread
import time


class SpiderThreadings(object):

    def cnki_task(self):
        cnki = CnkispaceSpider()
        cnki.pandas_save_data()
        time.sleep(2)

    def cqvip_task(self):
        cq = CqvipSpider()
        cq.pandas_save_data()
        time.sleep(2)

    def wanfang_task(self):
        wf = WFdataspider()
        wf.pandas_save_data()
        time.sleep(2)


def main():
    sp = SpiderThreadings()
    th1 = Thread(target=sp.cnki_task())
    th2 = Thread(target=sp.cqvip_task())
    th3 = Thread(target=sp.wanfang_task())
    th1.start()
    th2.start()
    th3.start()


if __name__ == '__main__':
    main()
