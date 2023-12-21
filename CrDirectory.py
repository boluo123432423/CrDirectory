# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import os
# from colorama import Fore
import urllib
from urllib import parse
import argparse


file_type_count = {}

def get_file_info(url, file_path):
    file_response = requests.head(url)
    content_length = file_response.headers.get("Content-Length")
    filename = os.path.basename(url)

    filetype = filename.split(".")
    filetype = filetype[-1]
    filetype = filetype.lower()
    if filetype in file_type_count:
        file_type_count[filetype] += 1
    else:
        file_type_count[filetype] = 1

    print(f"文件名：{urllib.parse.unquote(filename)}，\n大小：{content_length} 字节，路径：{base_url+'/'+urllib.parse.unquote(file_path)+urllib.parse.unquote(filename)}")
    print()

def crawl_website(url, old_path,file_path=""):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href == old_path :
            break
        new_url = f"{url}/{href}"
        if href.endswith("/"):
            print(href+"是文件夹")

            folder_path = os.path.join(file_path, href)
            crawl_website(new_url, file_path, folder_path)
        else:
            print(href + "不是文件夹")
            get_file_info(new_url, file_path)

parser = argparse.ArgumentParser(description='检测一个url')
parser.add_argument('-u', type=str, help='目标url  使用: -u http://127.0.0.1')
args = parser.parse_args()
base_url = args.u.split('\n')[0]
if args.u:
    crawl_website(base_url,'/')
for file_type, count in file_type_count.items():
    print(f"{file_type}: {count} 个文件")
