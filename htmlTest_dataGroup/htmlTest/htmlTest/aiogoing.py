import os

import aiohttp
import asyncio
import time
from http import cookies

import certifi
import slack as slack


async def set_cookies(cookie, url):
    temp_cookie = cookies.SimpleCookie()
    name = cookie.get('name', '')
    value = cookie.get('value', '')
    domain = cookie.get('domain', url)
    path = cookie.get('path', '/')
    expires = cookie.get('expires', int(time.time()) + 1000)

    if name != '' and value != '':
        temp_cookie[name] = value
        temp_cookie[name]['path'] = path
        temp_cookie[name]['domain'] = domain
        temp_cookie[name]['expires'] = expires

    return temp_cookie


async def request_(url, req_headers, req_cookies, func, req_body, filename):
    print(url + "进入测试")
    cookies_dic = {}
    # data = {}
    for cookie in req_cookies:
        temp_cookie = await set_cookies(cookie, url)
        cookies_dic[cookie['name']] = temp_cookie

    session = aiohttp.ClientSession(cookies=cookies_dic)
    # if func == 'PUT':
    #     data[file['filename']] = file['file_content']
    if func == 'POST' or func == 'PUT':
        if isinstance(req_body, dict):
            data = {}
            if filename:
                file_path = os.path.join(
                    "/Users/blinger/PycharmProjects/pythonProject/html_test/htmlTest_dataGroup/htmlTest/tempfiles_dir/",
                    filename)
                file = open(file_path, 'rb')
                data[filename] = file
            data.update(req_body)
        else:
            data = req_body
    else: data = ''

    start = time.time()
    resp = await session.request(func, url, headers=req_headers, data=data)
    end = time.time()
    rtt = int((end - start) * 1000)

    if filename:
        file.close()

    status = resp.status

    resp_cookies = []
    for _, cookie in resp.cookies.items():
        resp_cookies.append(str(cookie.output(header='')))

    resp_headers = []
    for name, value in resp.headers.items():
        header_dic = {
            name: value
        }
        resp_headers.append(header_dic)

    content = await resp.text()

    ret_dic = {
        'url': url,
        'func': func,
        'req_headers': req_headers,
        'req_cookies': req_cookies,
        'status': status,  # int
        'RTT': rtt,  # int
        'resp_headers': resp_headers,  # list[dic{}]
        'resp_cookies': resp_cookies,  # list[dic{}]
        'body': str(content).encode('utf-8')
    }
    print(url + '结束测试')

    return ret_dic