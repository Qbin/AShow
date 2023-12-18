#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/13 20:00
# @File    : llm.py
import os

import openai


def get_chat_completions_data(
        messages,
        return_count=1,
        max_tokens=4000,
        stream=False,
        temperature=0.6,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
):
    base_config = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "stream": stream,
        "n": return_count,
    }

    base_config.update(
        {
            "engine": "gpt-35-turbo",
            "api_type":  os.environ.get("OPENAI_API_TYPE"),
            "api_base": os.environ.get("OPENAI_API_BASE"),
            "api_version": os.environ.get("OPENAI_API_VERSION"),
            "api_key": os.environ.get("OPENAI_API_KEY"),
        }
    )
    response = openai.ChatCompletion.create(**base_config)
    return response["choices"][0]["message"]["content"]

if __name__ == '__main__':
    # K-means聚类算法的结果如何用热力图展示，带等高线的那种，给出python样例
    content = """下面文字中，一共提到了几个展览，分别是什么，请准确给出展览的开始时间（start_time）、结束时间（end_time）、地点(location)、票价（price）和名称(name)，并以json形式返回。
    收藏版北京12月份艺术展览推荐仓仓过河泥人过河泥人微信号guoheniren功能介绍始终热爱生活发表于本期为大家推荐2023年北京12月份艺术展汇总点击图片可查看展览详情观展前大家可在官方平台查看展览开放详情计划好行程观展展至名称地址详情待定仇世杰:黑色空中大丽花798艺术区拾萬空间12.5欧洲油画艺术珍藏展云上美术馆12.10所念皆山798艺术区当代唐人艺术中心12.10路之歌：铁扬艺术60元清华大学艺术博物馆12.12哪也不去798艺术区第零空间12.12漫长的漂浮aye画廊12.13绣在青海中国工艺美术馆12.16王赫：极目之游798艺术区蜂巢艺术12.16大卫杜阿尔：严肃的蛞蝓策略798艺术区魔金石空间12.17视觉爆炸的感官音乐798艺术区e03gallery12.17庞贝神话79元起国家图书馆国家典籍博物馆12.19冬，春夏秋lensgallery1958园区41212.20毛焰松美术馆12.20守正创新中国工艺美术馆12.20有世界名可爱游戏798艺术区共同艺术中心12.20繁简之思798艺术区三远当代艺术12.22好像有什么不对劲可能有书综合阅读空间12.27赤足hi艺术中心12.27无象修辞798艺术区方圆美术馆12.28双夜798艺术区新氧艺o2art12.29郊区outskirts798艺术区蔡锦空间12.29明清宫廷花卉题材文物展保利艺术博物馆12.30难以名状798艺术区tabularasa三米画廊12.30生命礼赞x螺旋航行798艺术区索卡艺术黑玫瑰与白玫瑰798艺术区丹麦文化中心12.31冬日变奏798艺术区灿艺术中心12.31宋庄搭子树美术馆12.31无限的剧场细江英公摄影展35元起三影堂摄影艺术中心12.31假期hiartspace12.31圣牛的消亡三影堂摄影艺术中心1.2没有边界的花园798艺术区頌艺术中心1.6削悄798艺术区北京公社1.7齐星：往事798艺术区偏锋画廊1.7与幽眠哭蓟798艺术区協力空间1.7文物里的中国龙特展中华世纪坛1.8秩序中国新绘画案例研究798艺术区又生空间1.9四季之竹egg画廊1.14菩萨蛮798艺术区墨方mocube1.15日常与潜在798艺术区lcegallery1.17严谨背后的松弛松美术馆1.18朴拙圆满悠艺术中心1.21皮囊之上红砖美术馆1.21离宫别馆798艺术区星空间stargallery1.21她他居住的国度798艺术区spursgallery1.31猿山修工作展monstore郎园stationa342f2.3七步之阶798艺术区户尔空间2.4花骨798艺术区空间站2.5幸运着15元起摩卡艺术中心2.5元素小说美凯龙艺术中心2.24汉化版本从中关村出发的数字生活共同体壹美美术馆2.25柏林国立博古睿美术馆馆藏展108元起798艺术区ucca尤伦斯当代艺术中心hnm2.25宇宙微尘航天互动艺术展59元起可以艺术馆2.25遇见印象派68元起798艺术区遇见博物馆2.25龍行天下興798艺术区ioma爱马思艺术中心2.25无限城市48元起798艺术区山中天艺术中心2.27域绘场48元北京时代美术馆2.29你好！三星堆隆福美术馆2.29邂逅三星堆751dpark普辣斯光影馆2.29异兽录：山海觅境南池子美术馆2.30甄嬛传文化传承体验特展798艺术园区a07馆3.2何翔宇798艺术区空白空间3.3nicedog798艺术区木木美术馆3.3智能秩序smartorder69artcampus3.10澄凝琼英故宫博物院藏玻璃精品展60元起嘉德艺术中心3.31环游世界艺术史朝阳大悦城10f3.31剧变生态798艺术区现代汽车文化中心4.7从纸到纸798艺术区长征空间12.204.7遇见古蜀三星堆78元起798艺术区遇见博物馆4.31文化创新洪流中美术思潮宋庄美术馆5.1尺素情怀清华学人手札展60元清华大学艺术博物馆5.8知觉的世界罗密欧ai朱丽叶88元起利星行中心a座北一层1.137.13文明的融合：驼铃声响民生现代美术馆文末赠票遇见高迪：天才建筑师的艺术世界文末赠票寻找与i人和e人最合拍的艺术家，莫奈梵高与现代主义大师真迹展文中图片来源其他账号，如有侵权，请联系我进行删除看展探店内容在小仓仓的理想生活更新，欢迎关注预览时标签不可点微信扫一扫关注该公众号轻触阅读原文继续滑动看下一个知道了微信扫一扫使用小程序取消允许取消允许：，。视频小程序赞，轻点两下取消赞在看，轻点两下取消在看
    """
    message = [
        {"role": "user", "content": content},
    ]
    print(get_chat_completions_data(messages=message))
