# -*- coding: utf-8 -*-
#Name: TinySpider
#Version: 1.0.2
#Author: chaif
#Author-email: admin at cfishacker com
#Home-page: https://github.com/cforth/TinySpider
#Summary: A simple web spider using Python 3.4
#License: MIT

import sys
import urllib.request
import chardet          #检测网页编码模块
import re               #正则表达式模块
import codecs           #处理字符编码模块
import json             #持久化对象模块
import time             #时间模块，用于测试运行时间

def print_list(the_list):
    """格式化输出列表（非嵌套）
    """
    if len(the_list) == 0:
        print('')
    else:
        for each_item in the_list:
            print(each_item)

def print_dict(the_dict, indent=False, level=0):
    """格式化打印出嵌套的字典对象,如果最终值为列表时，使用print_list打印列表
    indent默认为False，不打开缩进特性
    缩进级别level默认为0
    """
    for key, value in list(the_dict.items()) :
        if isinstance(value, dict):
            print('%s:' % key)
            print_dict(value, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t', end='')             
            print('%s:' % key, end='')
            if isinstance(value, list):
                print_list(value)
            else:
                print(value)
    print('\n')


def get_url_info(url):
    """抓取网页内容
    网页请求头部为Chrome信息，被抓取网页的编码为gb2312。
    返回包含网页内容的字符串。
    """
    user_agent = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.6 Safari/537.36'
    req = urllib.request.Request(url)
    req.add_header('User-Agent', user_agent)

    data = urllib.request.urlopen(req).read()     #抓取网页
    html_code = chardet.detect(data)              #通过chardet模块检测编码
    return data.decode(html_code['encoding'])     


def match_text(text, rules):
    """根据正则表达式匹配目标文本
    text为被分析的文本字符串。
    text去除每行行首与行尾空白字符、空行
    rules为一个字典，键为匹配目标名称，值为匹配规则（正则表达式字符串）。
    函数返回一个字典，键为匹配目标名称，值为符合匹配规则的字符串列表。
    """
    text = re.sub('\s*\n\s*','', text)            #去除每行行首与行尾空白字符、空行
    
    find_dict = {}
    
    for key in rules :
        s = re.findall(rules[key], text)
        find_dict[key] = s

    return find_dict   


class Spider():
    """网页爬虫类
    从标准输入获取网址url_head、起始页序号start、终止页序号end
    self.finds为存储抓取结果的字典
    """
    def __init__(self, rules, url_head, start, end, finds = {}, delaySecs=0):
        self.rules = rules
        self.url_head = url_head
        self.start = start
        self.end = end
        self.delaySecs = delaySecs
        self.finds = finds

    def catch(self):
        """根据匹配规则批量抓取一些网页
        顺序为页码从小到大，函数返回一个包含所有匹配目标信息的字典。
        """
        the_page = 1
        pages = self.end - self.start + 1
        for i in range(self.start, self.end + 1, 1):
            try:
                if str(i) not in self.finds:                                    #判断需抓取的页面是否已经抓取过，抓取过不重复抓取
                    text = get_url_info(self.url_head + str(i))
                    find_dict = match_text(text, self.rules)
                    self.finds[str(i)] = find_dict
                    print('页面抓取成功！页面号：{0}'.format(str(i)))
                    time.sleep(self.delaySecs)                                  #设置每次抓取的延时，默认为0秒
                else:
                    print('页面抓取结果已存在！不重复抓取！页面号：{0}'.format(str(i)))
            except:
                print('网页获取失败！错误信息：{0}'.format(sys.exc_info()[0]))
            print('任务进度({0}/{1})'.format(str(the_page), str(pages)))
            the_page += 1
            
    def save_finds(self, file_name):
        """将抓取结果字典finds写入磁盘文件,格式为JSON
        """
        try:
            with codecs.open(file_name, 'w', 'utf-8') as f:
                f.write(json.dumps(self.finds))
            print('对象保存成功！文件路径:{0}'.format(file_name))
        except:
            print('对象保存失败！错误信息：{0}'.format(sys.exc_info()[0]))

    def load_finds(self, file_name):
        """将finds对象从磁盘读取并恢复
        """
        try:
            with codecs.open(file_name, 'r', 'utf-8') as f:
                self.finds = json.loads(f.read())
            print('对象读取成功！文件路径:{0}'.format(file_name))
        except:
            print('对象读取失败！finds对象不变！错误信息：{0}'.format(sys.exc_info()[0]))

    
# end
