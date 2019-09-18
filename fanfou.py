import os
import requests
from pyquery import PyQuery as Pq
import save
import config
from utils import log


class Model:
    """
    显示类的信息
    """
    def __repr__(self):
        name = self.__class__.__name__
        properties = ['{}=({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Fanfou(Model):
    """
    存储消息信息
    """
    def __init__(self):
        # self.name = ''
        self.content = ''
        self.time = ''
        self.device = 'web'
        self.link = ''
        self.pic = ''
        self.pic_link = ''
        # self.ranking = 0


def get(url, filename):
    """
    模拟登陆并建立文件夹
    """
    phpsessid = config.cookie
    headers = {
        'Host': 'fanfou.com',
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'Referer': 'fanfou.com/home',
        'Cookie': 'PHPSESSID=' + phpsessid,
    }

    folder = 'cached'
    # 建立 cached 文件夹
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url, headers=headers)
        page = r.content
        with open(path, 'wb') as f:
            f.write(page)
            return page


def fanfou_from_div(div):
    """
    从 div 中获取消息信息
    """
    e = Pq(div)
    # 小作用域变量用单字符
    m = Fanfou()
    # m.name = e('.title').text()
    m.content = e('.content').text()
    m.time = e('.time').attr('stime')
    m.device = e('.method').text()
    m.link = "fanfou.com" + e('.stamp').html().split('"', 2)[1]
    m.pic_link = e('.content a').attr('name')
    if m.pic_link is not None:
        m.pic_link = 'fanfou.com' + m.pic_link
    m.pic = e('.photo').attr('href')
    m.pic = str(m.pic).split('@', 1)[0]
    # log('piclink', m.pic_link)
    return m


def fanfou_from_url(url):
    """
    从 url 下载并解析消息
    """
    page = cached_page(url)
    e = Pq(page)
    items = e('.message li')
    log('消息来自', items)
    # items[0]('title')
    # 调用 movie_from_div
    # __iter__ 迭代器
    f = [fanfou_from_div(i) for i in items]
    for i in f:
        f = i.__dict__
        save.SQLsave(f)
        if f['pic'] != 'None':
            pic = f['pic']
            log('保存照片', pic)
            save_pic(pic)

    return Fanfou


def save_pic(pic):
    """
    保存图片
    """
    file_name = str(pic).split('/')[-1]
    folder = 'img'
    # 建立 img 文件夹
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, file_name)

    r = requests.get(pic)
    with open(path, 'wb') as f:
        f.write(r.content)


def cached_page(url):
    """
    保存缓存页面
    """
    filename = '{}.html'.format(url.split('/')[-1])
    page = get(url, filename)
    return page


def get_last_page(url):
    """
    获取总页数
    """
    first_page = get(url, 'home')
    e = Pq(first_page)
    lastpage = e('.paginator').html().split('/p.')[-1].split('"', 1)[0]
    return int(lastpage)


def main():
    first_page = 'http://fanfou.com/{}/p.1'.format(config.username)
    last_page = get_last_page(first_page)
    log('共有{}页'.format(last_page))
    for i in range(1, last_page+1):
        url = 'http://fanfou.com/{}/p.{}'.format(config.username, i)
        fanfou_from_url(url)
        log('正在保存第 {} 页'.format(i))
    log('保存完成')


if __name__ == '__main__':
    main()
