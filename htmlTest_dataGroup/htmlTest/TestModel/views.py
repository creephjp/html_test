from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from . import models
# Create your views here.
from pandas.tests.io.excel.test_xlrd import xlrd


# def post(self, request, *args, **kwargs):
#     form = UploadExcelForm(request.POST, request.FILES)
#     if form.is_valid():
#     wb = xlrd.open_workbook(
#     filename=None, file_contents=request.FILES['excel'].read()) # 关键点在于这里
#     table = wb.sheets()[0]
#     row = table.nrows
#     for i in xrange(1, row):
#         col = table.row_values(i)
#     print (col)
#     return HttpResponse("ok")
# def post(self, request, *args, **kwargs):
#     form = UploadExcelForm(request.POST, request.FILES)
#     if form.is_valid():
#     wb = xlrd.open_workbook(
#     filename=None, file_contents=request.FILES['excel'].read()) # 关键点在于这里
#     table = wb.sheets()[0] row = table.nrows
#     for i in xrange(1, row):
#         col = table.row_values(i)
#         print (col)
#     return HttpResponse("ok")
import os


def upload(request):
    if request.method == 'POST':# 获取对象
        obj = request.FILES.get('fafafa')
        f = open(os.path.join('C:\python_workspace\htmlTest_dataGroup\csv_dir', 'static', 'pic', obj.name), 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        return  HttpResponse('OK')
    return render(request, 'upload/upload.html')