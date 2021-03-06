"""htmlTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
# from . import search2, views
# from htmlTest_dataGroup.htmlTest.htmlTest import search2, views
from . import search2, views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^search-post$', search2.search_post),
    path('main/', search2.search_post),
    path('form-input/', views.single_start),
    path('index/', search2.search_post),
    path('main/muit/',views.muit),
    path('muit/',views.muit),
    url(r'^$', views.hello),
    path('uploadFile/', views.upload_file),
    path('form-input/muit/', views.muit),
    path('download/', views.download),
    # path('muit.', views.muit),

]
# "User-Agent:Agent"
