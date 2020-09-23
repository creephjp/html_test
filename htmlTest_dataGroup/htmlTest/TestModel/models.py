from django.db import models

# Create your models here.
class Test(models.Model):
    #request属性
    req_headers = models.CharField(max_length=999,default='SOME STRING')
    req_cookies = models.CharField(max_length=999,default='SOME STRING')
    url = models.CharField(max_length=999,default='SOME STRING')
    func = models.CharField(max_length=20,default='SOME STRING')
    # response属性
    resp_headers = models.CharField(max_length=999,default='SOME STRING')
    body = models.TextField(max_length=99,default='SOME STRING')
    resp_cookies = models.CharField(max_length=999,default='SOME STRING')
    status = models.CharField(max_length=999,default='SOME STRING')
    RTT = models.CharField(max_length=999,default='SOME STRING')