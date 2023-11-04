"""
pip3 install requests lxml bs4
"""

import requests
from lxml import etree

class Spider:
    def __init__(self) -> None:
        # 数据文件保存位置
        self.__file='goods.txt'
        # 采集网站的地址:上传到hadoop000主机后把ip地址修改为shopxo的内网地址
        self.__site="http://172.18.21.2/index.php?s=/index/goods/index/id/{}.html"
        # 采集的商品的最大id
        self.__maxID=1277
        pass

    # 采集方法
    def __spider(self,url):
        header={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
        }
        # 发起GET请求
        response=requests.get(url,headers=header)
        # 判断状态码
        if response.status_code==200:
            # 对应的url是否有商品
            if "资源不存在或已被删除" in response.text:
                print(f"请求的地址{url}不存在商品！")
                return None
            else:
                # response -> html
                html=etree.HTML(response.text)
                # 定位页面元素：商品ID、名称、价格（销售价）、浏览量、销量、库存
                # 名称
                name=html.xpath('//h1[@class="detail-title am-margin-bottom-xs"]/text()')[0].strip()
                # 价格
                price=html.xpath('//b[@class="goods-price"]/text()')[0]
                # tm-count
                counts=html.xpath('//span[@class="tm-count"]/text()')
                # 销量
                sale=counts[0]
                # 浏览量
                view=counts[1]
                # 库存
                stock=html.xpath('//span[@class="stock"]/text()')[0]

                contents=f"{name},{price},{view},{sale},{stock}\n"

                return contents
        else:
            print(f"请求页面出现问题，状态码为:{response.status_code}!")
        

    def run(self):
        # 打开文件
        file=open(self.__file,"a+",encoding="utf-8")
        for page in range(1,self.__maxID+1):
            contents=self.__spider(self.__site.format(page))
            if contents:
                result=str(page)+","+contents
                file.write(result)

        # 关闭文件
        file.close()

# 程序入口
if __name__=="__main__":
    spider=Spider()
    spider.run()