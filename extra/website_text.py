#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/13 14:31
# @File    : website_text.py
import re

import requests
from bs4 import BeautifulSoup

from extra.llm import get_chat_completions_data


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


def test_get_all_text(url):
    res = get_all_text(url)
    return clear_character(res)


def test_llm(url):
    res = get_all_text(url)
    content = clear_character(res)

    if content:
        content = "下面文字中，准确给出展览的开始时间（start_time）、结束时间（end_time）、地点(location)、票价（price）和名称(name)，并以json形式返回，若某个字段未提及，则返回空值期望格式[{{}}]。\n {}".format(
            content)
        message = [
            {"role": "user", "content": content},
        ]
        return get_chat_completions_data(messages=message)


if __name__ == '__main__':
    # 用实际的网页URL调用函数
    url = 'https://mp.weixin.qq.com/s/6KUUuQ9M3pI-v6QoRX02WA'
    print("========================get_all_text=========================")
    website_text = test_get_all_text(url)
    print(website_text)
    print("========================llm=========================")
    show_list = test_llm(url)
    print(show_list)
