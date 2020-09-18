POST = {
    'req_headers': '''Connection: keep-alive
            User-Agent: 2020Man'''
                   ,
    'req_cookies': '''{
            "name": "cookie1",
            "value": "val1"
        };
        {
            "name": "cookie2",
            "value": "val2"
        };
        {
            "name": "cookie3",
            "value": "val3"
        }''',
    # 'url': 'http://example.com',
    'url': 'http://httpbin.org/put',
    'func': 'PUT',
    'body': '',
    'data_format': 'file'
}
FILES = {
    'filename': 'request.py',
    'file_content': open('request.py', 'rb')
}

data_list = [
{
    'headers': '''Connection: keep-alive
            User-Agent: 2020Man'''
                   ,
    'cookies': '''{
            "name": "cookie1",
            "value": "val1"
        };
        {
            "name": "cookie2",
            "value": "val2"
        };
        {
            "name": "cookie3",
            "value": "val3"
        }''',
    # 'url': 'http://example.com',
    'url': 'http://httpbin.org/get',
    'func': 'GET',
    'body': ''
},
{
    'headers': '''Connection: keep-alive
            User-Agent: 2020Man'''
                   ,
    'cookies': '''{
            "name": "cookie4",
            "value": "val4"
        };
        {
            "name": "cookie5",
            "value": "val5"
        };
        {
            "name": "cookie5",
            "value": "val5"
        }''',
    # 'url': 'http://example.com',
    'url': 'http://httpbin.org/post',
    'func': 'POST',
    'body': 'key1=value1',
    'data_format': 'raw'
}
]


