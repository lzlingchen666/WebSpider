import requests
from lxml import etree
import random
import time
from multiprocessing import  Pool
import pymongo

#构建Mongodb
client = pymongo.MongoClient('localhost',27017)
mydb = client['lingchen']
carrotchou = mydb['carrotchou']

#构建一个头部
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.116 Safari/537.36'
}

#链接列表
urls = ['http://www.carrotchou.blog/page/{}'.format(str(i)) for i in range(1,66)]

#抓取信息的方法
def get_message(url):
    html = requests.get(url,headers=headers)
    selector = etree.HTML(html.text)
    items = selector.xpath('/html/body/section/div[1]/div/article')
    for item in items:
        soft_class = item.xpath('header/a/text()')[0]
        soft_name = item.xpath('header/h2/a/text()')[0]
        release_time = item.xpath('p[1]/time/text()')[0]
        try:
            say_good = item.xpath('p[1]/a[2]/span/text()')[0]
        except:
            say_good = item.xpath('p[1]/a/span/text()')[0]
        introduction = item.xpath('p[2]/text()')[0]
        message = {
            '软件名':soft_name,
            '分类':soft_class,
            '发布时间':release_time,
            '点赞':say_good,
            '简介':introduction
        }
        print('正在抓取',soft_name,'的信息......')
        carrotchou.insert_one(message)
    sleep = random.randint(1,10)
    print('沉睡',sleep,'秒......')
    time.sleep(sleep)

if __name__ == '__main__':
    #创建一个线程池
    pool = Pool(processes=4)
    #创建映射
    pool.map(get_message,urls)
    # for url in urls:
    #     print('开始抓取',url,'的信息......')
    #     get_message(url)