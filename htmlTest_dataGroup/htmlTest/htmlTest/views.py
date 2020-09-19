import os
import time

import requests
from django.http import HttpResponse
from django.shortcuts import render
from TestModel.models import Test
import asyncio
import re
import json
import logging
from . import testdb
from TestModel import models

# from . import regoing
from . import regoing
from .init import split_form


# 用例导入
def hello(request):
    return render(request, 'main.html')

# def upload(request):
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     if request.method == 'POST':# 获取对象
#         obj = request.FILES.get('fafafa')
#         f = open(os.path.join(BASE_DIR, 'static', 'pic', obj.name), 'wb')
#         for chunk in obj.chunks():
#             f.write(chunk)
#         f.close()
#         return HttpResponse('OK')
#     return render(request, "index.html")

def muit(request):
    return render(request, 'muit.html')




def split_headers(str_headers):
    if str_headers != '':
        dic_headers = {}
        str_headers = re.sub(' ', '', str_headers)
        list_raw = str_headers.split('\n')
        # print(list_raw)
        for item in list_raw:
            kv_list = item.split(':')

            dic_headers[kv_list[0]] = kv_list[1]
    else:
        dic_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Connection': 'keep-alive',
        }

    return dic_headers


def split_form(str_form):
    if str_form != '':
        dic_form = {}
        str_body = re.sub(' ', '', str_form)
        list_raw = str_body.split('\n')
        for item in list_raw:
            kv_list = item.split(':')
            dic_form[kv_list[0]] = kv_list[1]
    else:
        dic_form = {}

    return dic_form


def split_cookies(str_cookies, url):
    if str_cookies != '':
        cookies = []
        str_cookies = re.sub("'", '"', str_cookies)
        temp_cookies = re.sub('\n', '', re.sub(' ', '', str_cookies))
        cookie_list = temp_cookies.split(';')
        print(cookie_list)
        for item in cookie_list:
            # print(type(item))
            cookie = json.loads(item)
            if 'url' not in cookie.keys():
                cookie['url'] = url
            # 设置到期时间
            # if 'expires' not in cookie.keys():
            #     cookie['expires'] = int(time.time()) + 3600
            cookies.append(cookie)
    else:
        cookies = []

    return cookies


def is_json(myjson):
 try:
  json_object = json.loads(myjson)
 except ValueError as e:
    return False

 return True


def single_start(request): # request
    # 获取需要解析网页的url及请求方式，如POST｜GET等
    print(str(request.POST))
    if request.POST:
        url = request.POST['url']
        func = request.POST['func']
    else:
        url = ''
        func = ''
    # 获取request中所传输的数据，比如需要设置的headers参数和cookie信息
    str_headers = request.POST.get('request-content-header', '')
    req_headers = split_headers(str_headers)
    str_cookies = request.POST.get('request-content-cookie', '')
    req_cookies = split_cookies(str_cookies, url)

    # 设置并发队列
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # 不同的请求再调用不同的处理函数
    if (func == 'POST' or func == 'PUT') and url != '':
        data_format = request.POST.get('data_format', '')
        print("提交方式为：" + str(data_format))
        if data_format == 'raw':
            body = request.POST.get('request-content-body', '')
            # 根据用户输入body格式进行处理提交格式
            if is_json(body):
                req_headers['Content-Type'] = 'application/json'
            else:
                req_headers['Content-Type'] = 'text/xml'

            result = asyncio.get_event_loop().run_until_complete(regoing.requests_(url, req_headers, req_cookies, func, body, {}))
            # result = {}
            return render(request, "main.html", result)
        else:
            # 处理表单
            str_form = request.POST.get('request-content-body', '')
            print(str_form)
            form = split_form(str_form)
            # 处理所传输的文件
            filename = request.FILES.get('filename', '')
            file_content = request.FILES.get('file_content', '')
            if filename == '':
                files = {}
            else:
                files = {
                    filename: file_content
                }
            result = asyncio.get_event_loop().run_until_complete(
                regoing.requests_(url, req_headers, req_cookies, func, form, files))
            return render(request, "main.html", result)
    elif (func == 'GET' or func == 'DELETE') and url != '':
        result = asyncio.get_event_loop().run_until_complete(regoing.requests_(url, req_headers, req_cookies, func, {}, {}))
        # testdb(**result)
        models.Test.objects.create(**result)
        return render(request, "main.html", result)


# def many_start(data_list):
#     # url=[''] func=[''] headers=[{}] cookies[[{}]] body[""]
#
#     get_delete_tasks = []
#     post_raw_tasks = []
#     post_other_tasks = []
#
#     for req in data_list:
#         # 处理headers,cookies,form
#         print("into for")
#         print(req)
#         url = req.get('url')
#         func = req.get('func')
#         req_headers = split_headers(req.get('headers', ''))
#         req_cookies = split_cookies(req.get('cookies', ''), req.get('url'))
#         if url != '' and (func == 'GET' or func == 'DELETE'):
#             print("into get")
#             get_delete_tasks.append(asyncio.ensure_future(pptrgoing.requests_(url, req_headers, req_cookies, func)))
#         elif url != '' and func == 'POST':
#             print("into post")
#             data_format = req.get('data_format', '')
#             req_body = req.get('body', '')
#             if data_format == 'raw':
#                 post_raw_tasks.append(asyncio.ensure_future(
#                     pptrgoing.requests_(url, req_headers, req_cookies, func, req_body)))
#             elif data_format == 'kv':
#                 post_other_tasks.append(asyncio.ensure_future(
#                     regoing.requests_(url, req_headers, req_cookies, func, req_body, {})))
#
#     if post_other_tasks: asyncio.get_event_loop().run_until_complete(asyncio.wait(post_other_tasks))
#     if post_raw_tasks: asyncio.get_event_loop().run_until_complete(asyncio.wait(post_raw_tasks))
#     if get_delete_tasks: asyncio.get_event_loop().run_until_complete(asyncio.wait(get_delete_tasks))
