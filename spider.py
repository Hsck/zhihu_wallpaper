import re
import os
import requests
from multiprocessing import Pool
import time

headers = {
    'accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/question/34537281',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    'X-UDID': 'AFBC56GCmQyPTvddMtByG7-ExQNle8BUIxs='
    }


# 请求页面URL，结果返回页面内容
def get_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('成功得到页面')
            return response.text
    except Exception:
        print('error')
        return None


# 正则解析出图片的URL,对于列表里的每个图片URL，调用get_image_content()函数
def parse_page(data):
    pattern = re.compile('data-actualsrc=\\\\"(.*?)\\\\">', re.S)
    contents = re.findall(pattern, data)
    for content in contents:
        get_image_content(content)


# 请求图片URL，获取图片内容后调用save()函数
def get_image_content(image_url):
    response = requests.get(image_url)
    image = response.content
    # 图片名赋值为图片URL的后17位字符
    img_name = image_url[-17:]
    print('下载图片:', img_name)
    save(image, img_name)


# 保存图片到路径path
def save(image, img_name='rename', path='E:/wallpaper'):
    try:
        fpath = os.path.join(path, img_name)
        with open(fpath, 'wb') as f:
            f.write(image)
            f.close()
    except Exception:
        print('error')


def main(page):
    url = 'https://www.zhihu.com/api/v4/questions/29784516/answers?' \
           'include=data%5B*%5D.is_normal%2Ccan_comment%2Ccontent&sort_by=default&limit=20&offset=' + str(page)
    print('请求第 %d 页' % (int(page)/20 + 1))
    data = get_page(url)
    parse_page(data)
    time.sleep(2)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 20 for i in range(23)])

