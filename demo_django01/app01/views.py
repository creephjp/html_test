from django.shortcuts import render,HttpResponse
from app01 import models


def test(request):
    # models.UserType.objects.create(title='普通用户')
    # models.UserType.objects.create(title='二比用户')
    # models.UserType.objects.create(title='牛逼用户')
    # models.UserInfo.objects.create(name='方少伟',age=18,ut_id=1)
    # models.UserInfo.objects.create(name='黄金鹏',age=20,ut_id=2)
    # models.UserInfo.objects.create(name='苏柳', age=20, ut_id=3)

   # result = models.UserInfo.objects.all()
    # for obj in result:
    #     print(obj.name,obj.age,obj.ut_id,obj.ut.title,obj.ut.fo.caption)
    # for row in obj.userinfo_set.all():
    #     print(row.name,row.age)

    # obj = models.UserInfo.objects.all().first()
    # print(obj.name, obj.ut.title)

    # obj = models.UserType.objects.all().first()
    # print('用户类型',obj.id, obj.title)
    result = models.UserType.objects.all()
    for item in result:
        print(item.title)

    return HttpResponse('。。。')
from django.views import View
class Login(View):
    def get(self,request):
        return render(request, 'login.html',)
    def post(self,request):
        print(request.POST.get('user'))
        return HttpResponse('Login.post')