# -*- coding:utf-8 -*-
import hashlib
import re


def get_md5(url):
    '''
        处理MD5加密
    :param url:
    :return:
    '''
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    '''
    从字符串中提取出数字
    :param text:
    :return:
    '''
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


if __name__ == "__main__":
    print(get_md5("http://jobbole.com"))
