import  requests
from  lxml  import etree
from  multiprocessing import Pool
import  time
import random

urls = ['https://www.wallpapermaiden.com/random?page={}'.format(str(i)) for i in range(1,10)]

headers = {
    'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.116 Mobile Safari/537.36',
    'referer': 'https://www.wallpapermaiden.com/random'
}

num = 0
path = 'E://JetBrains/Pycharm/网络爬虫/WallPaper/'


def get_img(url):
    global num
    html = requests.get(url,headers = headers)
    selector = etree.HTML(html.text)
    items = selector.xpath('/html/body/div[2]/div/div[2]/div[2]/div/div')
    for item in items:
        try:
            img_url = 'https://www.wallpapermaiden.com' + item.xpath('a/div[1]/img/@src')[0].replace('-thumb','')
            fp = open(path+'WallPaper'+str(num)+str(random.randint(1000,10000))+'.jpg','wb')
            num+=1
            img = requests.get(img_url,headers = headers)
            fp.write(img.content)
            print(num,' 正在写入',img_url,'......')
            fp.close()
            print(num,img_url,'写入完成!')
        except:
            pass
    time.sleep(random.randint(1,8))

if __name__ == '__main__':
    pool = Pool(processes=4)
    pool.map(get_img,urls)
