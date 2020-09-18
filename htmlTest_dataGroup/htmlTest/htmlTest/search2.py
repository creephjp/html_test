# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf


# 接收POST请求数据
def search_post(request):
    ctx = {}
    if request.POST:
        ctx['rlt'] = request.POST['url']
        ctx['rlt2'] = request.POST['func']
    return render(request, "main.html", ctx)