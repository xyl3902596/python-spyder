#coding=utf-8
import re
import requests
from urllib import error
import os

def downloadPicture(num,html, keyword):
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 先利用正则表达式找到图片url
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片，图片地址:' + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载')
            continue
        else:
            string = os.path.join("pic",keyword,keyword + '_' + str(num) + '.jpeg')
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return num
    return num


def download_onepersion(word,id):
    url = 'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word='+word

    y = os.path.exists(os.path.join("pic",word))
    if y == 0:
        os.mkdir(os.path.join("pic",word))
    page=0
    num=0
    tmp = url
    print("搜索到第"+str(id+1)+"位女明星：" + word + '的图片，即将开始下载图片...'+"\n")
    while num < numPicture:
        try:
            url = tmp + str(page)
            result = requests.get(url, timeout=10)
        except error.HTTPError as e:
            print('网络错误，请调整网络后重试')
            page+=1
        else:
            num=downloadPicture(num,result.text, word)
            page+=1
    print(word+'的图片已经搜索结束\n')

if __name__=="__main__":
    with open("name.txt","r") as f:
        name_list=[name.strip().strip("\n") for name in f.readlines()]
    if not os.path.exists("pic"):
        os.mkdir("pic")
    n=int(input("你想要搜索几位女明星的照片:"))
    numPicture=int(input("每位女明星的照片数目："))
    for id in range(n):
        download_onepersion(name_list[id],id)
