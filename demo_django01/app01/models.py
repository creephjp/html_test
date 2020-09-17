from django.db import models

class UserType(models.Model):
    title = models.CharField(max_length=32)
    fo = models.ForeignKey('Foo',on_delete=models.CASCADE)

class UserInfo(models.Model):
     name = models.CharField(max_length=16)
     age = models.IntegerField()
     ut = models.ForeignKey('UserType',on_delete=models.CASCADE)

class Foo(models.Model):
    caption = models.CharField(max_length=32)