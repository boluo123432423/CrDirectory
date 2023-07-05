# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import urllib
from urllib import parse
import argparse


def get_file_info(url, file_path):
    # 发送 HEAD 请求获取文件大小
    file_response = requests.head(url)

    # 获取文件大小（以字节为单位）
    content_length = file_response.headers.get("Content-Length")

    # 获取文件名
    filename = os.path.basename(url)

    # 打印文件名、大小和访问路径
    print(f"文件名：{urllib.parse.unquote(filename)}，\n大小：{content_length} 字节，路径：{base_url+'/'+urllib.parse.unquote(file_path)+urllib.parse.unquote(filename)}")

def crawl_website(url, old_path,file_path="/"):
    # 发送 GET 请求获取网页内容
    response = requests.get(url)

    # 解析网页内容
    soup = BeautifulSoup(response.text, "html.parser")

    # 获取所有链接标签
    links = soup.find_all("a")

    # 遍历链接标签
    for link in links:
        # 获取链接的相对路径
        href = link.get("href")
        # 拼接完整 URL
        if href == old_path :# 判断是否为跳转上一级
            break
        url = f"{base_url}/{href}"

        # 判断是否为文件夹
        if href.endswith("/"):
            folder_path = os.path.join(file_path, href)
            crawl_website(url, file_path, folder_path)
        else:
            get_file_info(url, file_path)

# 开始爬取网站
parser = argparse.ArgumentParser(description='检测一个url')
parser.add_argument('-u', type=str, help='目标url  使用: -u http://127.0.0.1')
args = parser.parse_args()
base_url = args.u.split('\n')[0]
if args.u:
    crawl_website(base_url,'/')
