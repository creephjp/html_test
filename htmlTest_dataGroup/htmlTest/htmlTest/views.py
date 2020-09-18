import os
import time

import requests
from django.http import HttpResponse
from django.shortcuts import render

import asyncio
import re
import json
import logging

# from . import regoing
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


def single_start(request): # request
    # 获取需要解析网页的url及请求方式，如POST｜GET等
    if request.POST:
        url = request.POST['url']
        func = request.POST['func']
    else:
        url = ''
        func = ''
    # 获取request中所传输的数据，比如需要设置的headers参数和cookie信息
    # data_dic = get_data(request, url) # request
    # return HttpResponse(func)
    str_headers = request.POST.get('headers', '')
    req_headers = split_headers(str_headers)
    str_cookies = request.POST.get('req_cookies', '')
    req_cookies = split_cookies(str_cookies, url)
    # return HttpResponse(str(type(req_cookies)))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # req_cookies = asyncio.get_event_loop().run_until_complete(split_cookies(str_cookies, url))
    # return HttpResponse(req_cookies)
    # req_headers = data_dic['req_headers']
    # req_cookies = data_dic['req_cookies']
    # 不同的请求再调用不同的处理函数
    if (func == 'POST' or func == 'PUT') and url != '':
        data_format = request.POST['data_format']
        if data_format == 'raw':
            body = request.POST['body']
            # result = asyncio.get_event_loop().run_until_complete(pptrgoing.requests_(url, req_headers, req_cookies, func, body))
            result = {}
            return render(request, "main.html", result)
        else:
            # 处理表单
            str_form = request.POST['body']
            form = split_form(str_form)
            # 处理所传输的文件
            filename = request.FILES['filename']
            file_content = request.FILES['file_content']
            if filename == '':
                files = {}
            else:
                files = {
                    filename: file_content
                }
            result = asyncio.get_event_loop().run_until_complete(
                requests_(url, req_headers, req_cookies, func, form, files))
            return render(request, "main.html", result)
    elif (func == 'GET' or func == 'DELETE') and url != '':
        result = asyncio.get_event_loop().run_until_complete(requests_(url, req_headers, req_cookies, func, {}, {}))
        return render(request, "main.html", result)


   # tasks = [asyncio.ensure_future(your_function(url)) for url in urls]
    # asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))


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

async def set_cookies(s, kwargs):
    name = kwargs.get('name', '')
    value = kwargs.get('value', '')
    domain = kwargs.get('domain', '')
    path = kwargs.get('path', '')
    expiry = kwargs.get('expiry', int(time.time()))

    temp_cookie = requests.cookies.create_cookie(**{
        'name': name,
        'value': value,
        'domain': domain,
        'path': path,
        'expires': expiry,
    })

    # print(type(temp_cookie))
    s.cookies.set_cookie(temp_cookie)


async def requests_(url, req_headers, req_cookies, func, form, file):
    resp_cookies = []
    session = requests.Session()
    for cookie in req_cookies:
        await set_cookies(session, cookie)

    # print(session.cookies)
    # 发起请求并计算rtt
    start = time.time()
    if func == 'PUT':
        resp = session.request(method=func, url=url, headers=req_headers, cookies=session.cookies.get_dict(),
                               files=file)
    elif func == 'POST':
        if file:
            resp = session.request(method=func, url=url, headers=req_headers, cookies=session.cookies.get_dict(),
                                   data=form, files=file)
        else:
            resp = session.request(method=func, url=url, headers=req_headers, cookies=session.cookies.get_dict(),
                                   data=form)
    else:
        resp = session.request(method=func, url=url, headers=req_headers, cookies=session.cookies.get_dict())

    end = time.time()
    rtt = int((end - start) * 1000)
    # 请求状态码
    status = resp.status_code
    # print('status code: ' + str(status) + '\t' + 'RTT: ' + str(rtt) + 'ms')
    # 获取response cookie信息
    # print('------------cookies---------------')
    for cookie in session.cookies:
        name = cookie.name
        value = cookie.value
        domain = cookie.domain
        path = cookie.path
        secure = cookie.secure

        resp_cookies.append({
            'name': name,
            'value': value,
            'domain': domain,
            'path': path,
            'secure': secure
        })
        # print(f"{name} = {value}\t{domain}\t{path}\t{secure}")
    # 获取response headers
    resp_headers = resp.headers
    # print('------------headers---------------')
    # print(resp_headers)
    # for kv in resp_headers.items():
    #     # print(kv)
    #     print(f'{kv[0]} = {kv[1]}')
    # print(resp.text)
    # 获取response body
    content = resp.text
    # print(content)
    # 返回结果
    ret_dic = {
        'status': status,  # int
        'RTT': rtt,  # int
        'headers': resp_headers,  # dic
        'cookies': resp_cookies,  # list[dic{}]
        'body': content
    }

    return ret_dic