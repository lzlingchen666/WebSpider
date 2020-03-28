import requests
from lxml import etree
import time
import random
from  multiprocessing import Pool

#构建链接,总共是10页
urls = ['https://wallhaven.cc/toplist?page={}'.format(str(i))for i in range(1,10)]

#构建一个headers
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.116 Safari/537.36',
    'referer': 'https://wallhaven.cc/toplist?page=1'
}

#构建一个图片存放的父文件夹
path = 'E:/JetBrains/Pycharm/网络爬虫/WallPaper/wallhaven/'

#构建一个方法用来下载图片
def get_img(url):
    #请求一个页面内容
    html = requests.get(url,headers = headers)
    # time.sleep(2)
    #使用etree进行解析
    selector = etree.HTML(html.text)
    #获取图片的链接列表
    img_urls = selector.xpath('//*[@id="thumbs"]/section[1]/ul/li/figure/img/@data-src')
    #循环获取图片
    for img_url in img_urls:
        try:
            #打开一个文件,用来存放即将写入的图像数据
            fp = open(path+img_url.split('/')[-1],'wb')
            #请求图像数据
            img_data = requests.get(img_url.replace('th.','w.').replace('small','full').replace(img_url.split('/')[-1],'wallhaven-'+img_url.split('/')[-1]),headers = headers)
            #写入图片的二进制数据
            print('正在写入',img_url.split('/')[-1]+'......')
            fp.write(img_data.content)
            #关闭文件
            fp.close()
            print('写入',img_url.split('/')[-1]+'完成!')
            #创建一个休眠时间
            # time.sleep(random.randint(1,5))
        except:
            print(html.status_code)

if __name__ == '__main__':
    # #创建4个进程
    pool = Pool(processes=4)
    # # #进程映射方法
    pool.map(get_img,urls)
    # for url in urls:
    #     get_img(url)
