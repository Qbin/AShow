#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/13 14:31
# @File    : website_text.py
import re

import requests
from bs4 import BeautifulSoup


def get_all_text(url):
    # 发送HTTP请求获取网页内容
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取所有文本内容
        all_text = soup.get_text()

        # 打印或返回所有文本
        # print(all_text)
        return all_text
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None


def clear_character(sentence):
    """ 只保留汉字、字母、数字 """
    pattern = re.compile('[^，。！？.:：\u4e00-\u9fa5^a-zA-Z^0-9]')
    line = re.sub(pattern, '', sentence.lower())
    new_sentence = ''.join(line.split())  # 去除空白
    return new_sentence


if __name__ == '__main__':
    # 用实际的网页URL调用函数
    url = 'https://mp.weixin.qq.com/s/6KUUuQ9M3pI-v6QoRX02WA'
    res = get_all_text(url)
    print(clear_character(res))
