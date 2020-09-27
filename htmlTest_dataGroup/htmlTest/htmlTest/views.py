import os
import time
from csv import excel

import pandas
import requests
from django.http import HttpResponse, request
from django.shortcuts import render
from TestModel.models import Test
import asyncio
import re
import json
import logging
from . import testdb
from TestModel import models

from .aiogoing import request_
from .init import split_form, split_headers, split_cookies, is_json

file_results = []
# 用例导入


def hello(request):
    return render(request, 'main.html')


def muit(request):
    return render(request, 'muit.html')


# 下载测试结果
def download(request):
    # 创建文件路径
    file_path = os.path.join(
            "/Users/blinger/PycharmProjects/pythonProject/html_test/htmlTest_dataGroup/htmlTest/tempfiles_dir/",
            str(int(time.time()))+'.xlsx')

    # 生成文件
    pf = pandas.DataFrame(file_results[0])
    pf.fillna('', inplace=True)
    pf.to_excel(file_path, encoding='utf-8', index=False)

    # 返回文件
    file = open(file_path, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="result.xlsx"'
    return response


# 单url处理
def single_start(request):  # request
    # 获取需要解析网页的url及请求方式，如POST｜GET等
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
    # 不同的请求方式传入不同的Request参数
    if (func == 'POST' or func == 'PUT') and url != '':
        data_format = request.POST.get('data_format', '')
        # 用户所上传的Body为json、xml或字符串类型
        if data_format == 'raw':
            body = request.POST.get('request-content-body', '')
            # 根据用户输入body格式添加请求头
            if is_json(body):
                req_headers['Content-Type'] = 'application/json'
            else:
                req_headers['Content-Type'] = 'text/xml'

            # 调用模拟请求接口
            result = asyncio.get_event_loop().run_until_complete(
                request_(url, req_headers, req_cookies, func, body, {}))
            models.Test.objects.create(**result)
            # 根据测试结果渲染前端界面
            result['body'] = result['body'].decode('utf-8')
            return render(request, "main.html", result)
        else:
            # 处理表单
            str_form = request.POST.get('request-content-body', '')
            form = split_form(str_form)

            # 处理所传输的文件
            file = request.FILES.get('file', '')
            if file == '':
                file = ''
            else:
                filename = os.path.join(
                    "/Users/blinger/PycharmProjects/pythonProject/html_test/htmlTest_dataGroup/htmlTest/tempfiles_dir/", file.name)
                destination = open(filename, 'wb+')
                for chunk in file.chunks():
                    destination.write(chunk)

                destination.close()


            # 调用模拟请求接口
            result = asyncio.get_event_loop().run_until_complete(
                request_(url, req_headers, req_cookies, func, form, file))
            # 将结果保存至数据库
            models.Test.objects.create(**result)
            # 根据测试结果渲染前端界面
            result['body'] = result['body'].decode('utf-8')
            return render(request, "main.html", result)
    elif (func == 'GET' or func == 'DELETE') and url != '':
        # 调用模拟请求接口
        result = asyncio.get_event_loop().run_until_complete(
            request_(url, req_headers, req_cookies, func, {}, {}))

        # 存储到数据库
        models.Test.objects.create(**result)
        # 根据测试结果渲染前端界面
        result['body'] = result['body'].decode('utf-8')
        return render(request, "main.html", result)


# 接收用户所上传的批量测试文件
def upload_file(request):
    if request.method == "POST":
        # 接收用户所上传的批量测试文件
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return HttpResponse("no files for upload")
        filename1 = os.path.join(
            "/Users/blinger/PycharmProjects/pythonProject/html_test/htmlTest_dataGroup/htmlTest/tempfiles_dir",
            myFile.name)
        destination = open(filename1, 'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()

        # 将文件内容转换为列表，列表中的元素为字典，即一条测试数据
        results = excel(filename1)

        # 调用批量处理接口
        results = many_start(request, results)
        file_results.append(results)

        # 根据结果渲染前端界面
        return render(request, "muit.html", {'results': results})


# 处理表格数据
def excel(filename1):
    result_list = []
    try:
        sheet = pandas.read_excel(filename1, "Sheet1")
        print("表单长度为：" + str(len(sheet)))

        for row in sheet.index.values:
            docs = dict()
            docs['url'] = re.sub('nan', '', str(sheet.iloc[row, 0]))
            docs['func'] = re.sub('nan', '', str(sheet.iloc[row, 1]))
            docs['data_format'] = re.sub('nan', '', str(sheet.iloc[row, 2]))
            docs['headers'] = re.sub('nan', '', str(sheet.iloc[row, 3]))
            docs['cookies'] = re.sub('nan', '', str(sheet.iloc[row, 4]))
            docs['body'] = re.sub('nan', '', str(sheet.iloc[row, 5]))
            result_list.append(docs)

    except Exception as e:
        print(e)

    return result_list


# 批量测试接口
def many_start(request, data_list):
    # 初始化协程集合
    get_delete_tasks = []
    post_raw_tasks = []
    post_other_tasks = []
    results = []

    # 创建并设置事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # 处理请求数据并调用模拟请求接口
    for req in data_list:
        # 处理测试数据
        url = req.get('url')
        func = req.get('func')
        req_headers = split_headers(req.get('headers', ''))
        req_cookies = split_cookies(req.get('cookies', ''), req.get('url'))

        # 根据不同的请求方式调用不同的模拟请求接口
        if url != '' and (func == 'GET' or func == 'DELETE'):
            # 创建协程对象并封装为task，等待并发执行
            get_delete_tasks.append(asyncio.ensure_future(
                request_(url, req_headers, req_cookies, func, {}, {}))
            )
        elif url != '' and func == 'POST':
            data_format = req.get('data_format', '')
            req_body = req.get('body', '')
            if data_format == 'raw':
                # 创建协程对象并封装为task，等待并发执行
                post_raw_tasks.append(asyncio.ensure_future(
                    request_(url, req_headers, req_cookies, func, req_body, {}))
                )
            elif data_format == 'kv':
                req_body = split_form(req_body)
                # 创建协程对象并封装为task，等待并发执行
                post_other_tasks.append(asyncio.ensure_future(
                    request_(url, req_headers, req_cookies, func, req_body, {}))
                )

    # 通过事件循环调用协程函数，并发执行模拟请求
    if post_other_tasks: asyncio.get_event_loop().run_until_complete(asyncio.wait(post_other_tasks))
    if post_raw_tasks: asyncio.get_event_loop().run_until_complete(asyncio.wait(post_raw_tasks))
    if get_delete_tasks: asyncio.get_event_loop().run_until_complete(asyncio.wait(get_delete_tasks))

    # 将不同请求方式添加到一个列表中
    tasks_result = []
    tasks_result.extend(get_delete_tasks)
    tasks_result.extend(post_raw_tasks)
    tasks_result.extend(post_other_tasks)

    # 遍历每一个协程的执行结果
    for item in tasks_result:
        temp_result = item.result()
        # 保存至数据库
        models.Test.objects.create(**temp_result)
        temp_result['body'] = temp_result['body'].decode('utf-8')

        results.append(temp_result)

    return results
