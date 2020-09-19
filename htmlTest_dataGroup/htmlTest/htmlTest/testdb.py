from django.http import HttpResponse

from TestModel.models import Test

def testdb(request,**result):

    models.UserInfor.objects.create(**info)
    return HttpResponse('success')

