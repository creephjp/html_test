
import json
import re
# import request

# header、cookie、body需要做输入合法性检测


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


def get_data(request, url): # request
    if request.POST:
        str_headers = request.POST['req_headers']
        req_headers = split_headers(str_headers)

        str_cookies = request.POST['req_cookies']
        req_cookies = split_cookies(str_cookies, url)

        ret_dic = {
            'req_headers': req_headers,
            'req_cookies': req_cookies
        }

        return ret_dic




# single_start()
# many_start(request.data_list)