import requests
import time


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