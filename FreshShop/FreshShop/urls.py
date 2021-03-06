"""FreshShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path,include

from Buyer.views import index
from Store.views import GoodsViewSet
from Store.views import TypeViewSet

from rest_framework import routers








router = routers.DefaultRouter() #声明一个默认路由注册器
router.register(r"goods",GoodsViewSet) #注册写好的接口视图
router.register(r'goodsType', TypeViewSet) #注册写好的接口视图






urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include("ckeditor_uploader.urls")),
    path('store/', include("Store.urls")),
    path('buyer/', include("Buyer.urls")),
    re_path('^API',include(router.urls)), #restful的根路由
    re_path('^api-auth',include('rest_framework.urls')), #接口认证


]

urlpatterns += [
    re_path('^$', index),
]