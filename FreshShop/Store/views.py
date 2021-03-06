# coding:utf-8
import hashlib
import json

from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.models import *


# Create your views here.
def setPassword(password):  # 加密函数
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()


def register(request):  # 注册函数
    result = {"info": ""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        c_password = request.POST.get("confirm_password")
        if username and password and c_password:
            sql_username = Seller.objects.filter(username=username).first()
            if sql_username:
                result["info"] = "用户已存在"
                return render(request, "store/register.html", locals())

            else:
                if password == c_password:
                    Seller.objects.create(
                        username=username,
                        password=setPassword(password)
                    )
                    return HttpResponseRedirect("/store/login/")
                else:
                    result["info"] = "两次密码不相等"
        else:
            result["info"] = "注册信息不能为空"
    return render(request, "store/register.html", locals())


def loginValid(fun):  # 装饰器
    def inner(request, *args, **kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user:  # 用户名称cookie
            username = json.loads(c_user)
            if username == s_user:
                user = Seller.objects.filter(username=username).first()
                if user:  # 用户存在
                    store = Store.objects.filter(user_id=user.id).first()
                    response = fun(request, *args, **kwargs)
                    if store:
                        response.set_cookie("has_store", store.id)
                    else:
                        response.set_cookie("has_store", "")
                    return response
        return HttpResponseRedirect("/store/login/")

    return inner


# @loginValid
def login(request):  # 登录函数
    response = render(request, "store/login.html")
    response.set_cookie("login_form", "login_page")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            sql_username = Seller.objects.filter(username=username).first()
            if sql_username:  # 如果存在用户
                cookie = request.COOKIES.get("login_form")
                hex_password = setPassword(password)
                # 判断密码和登录来源
                if sql_username.password == hex_password and cookie == "login_page":
                    name = json.dumps(username)
                    response = HttpResponseRedirect("/store/index/")
                    response.set_cookie("username", name)
                    response.set_cookie("user_id", sql_username.id)  # cookie提供用户id方便其他功能查询
                    request.session["username"] = username
                    # 检测该用户是否有店铺
                    store = Store.objects.filter(user_id=sql_username.id).first()
                    if store:
                        response.set_cookie("has_store", store.id)
                    else:
                        response.set_cookie("has_store", "")
                    return response
    return response


def logout(request):
    response = HttpResponseRedirect("/store/login/")
    response.delete_cookie("has_store")
    response.delete_cookie("username")
    response.delete_cookie("user_id")
    response.delete_cookie("login_form")
    request.session.flush()

    return response


@loginValid
def index(request):
    user_id = request.COOKIES.get("user_id")
    if user_id:
        return render(request, "store/index.html", locals())
    return HttpResponseRedirect("/store/login/")


@loginValid
def register_store(request):
    type_list = StoreType.objects.all()
    if request.method == "POST":
        store_name = request.POST.get("store_name")
        store_address = request.POST.get("store_address")
        store_description = request.POST.get("store_description")
        store_phone = request.POST.get("store_phone")
        store_money = request.POST.get("store_money")

        user_id = int(request.COOKIES.get("user_id"))  # 通过cookie来得到user_id
        type_list = request.POST.get("type")  # 通过request.post得到类型，但是是一个列表

        store_logo = request.FILES.get("store_logo")  # 通过request.FILES得到图片文件

        # 保存非多对多数据
        store = Store()
        store.store_name = store_name
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo  # django1.8之后图片可以直接保存
        store.save()  # 保存，生成了数据库当中的一条数据

        # 在生成的数据当中添加多对多字段。
        for i in type_list:  # 循环type列表，得到类型id
            store_type = StoreType.objects.get(id=i)  # 查询类型数据
            store.type.add(store_type)  # 添加到类型字段，多对多的映射表
        store.save()  # 保存数据
        response = HttpResponseRedirect("/store/index/")
        response.set_cookie("has_store", store.id)
        return response
    return render(request, "store/register_store.html", locals())


@loginValid
def add_goods(request):
    goods_type = GoodsType.objects.all()
    if request.method == "POST":
        # 获取post请求
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_store = request.POST.get("goods_store")
        goods_image = request.FILES.get("goods_image")
        goods_type = request.POST.get("goods_type")  # 返回的是一个列表
        # 开始保存数据
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.goods_type_id = goods_type

        goods.save()
        # 保存多对多数据
        goods.store_id.add(
            Store.objects.get(id=int(goods_store))
        )
        goods.save()
        return HttpResponseRedirect("/store/goods_list/up/")
    return render(request, "store/add_goods.html", locals())

@loginValid
def list_goods(request, status):  # 分页展示所有商品并只展示本人店铺的
    if status == "up":
        state = 1
    else:
        state = 0

    keywords = request.GET.get("keywords")
    page_num = request.GET.get("page_num", 1)

    # 查询店铺
    store_id = request.COOKIES.get("has_store")
    store = Store.objects.get(id=int(store_id))
    if keywords:  # 判断关键词是否存在
        goods_list = store.goods_set.filter(goods_name__contains=keywords, goods_status=state)  # 完成了模糊查询

    else:  # 如果关键词不存在，查询所有
        goods_list = store.goods_set.filter(goods_status=state)

    # 分页
    paginator = Paginator(goods_list, 3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request, "store/goods_list.html", locals())

def goods_list_api(request):
    return render(request, "store/goods_list_api.html", locals())


@loginValid
def goods(request, goods_id):  # 商品详情
    goods_data = Goods.objects.filter(id=goods_id).first()
    return render(request, "store/goods.html", locals())


@loginValid
def update_goods(request, goods_id):  # 修改商品
    goods_data = Goods.objects.filter(id=goods_id).first()
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_store = request.POST.get("goods_store")
        goods_image = request.FILES.get("goods_image")
        # 开始修改数据
        goods = Goods.objects.filter(id=goods_id).first()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        if goods_image:
            goods.goods_image = goods_image
        goods.save()
        return HttpResponseRedirect("/store/goods/%s/" % goods.id)
    return render(request, "store/update_goods.html", locals())


def goods_status(request, state):
    if state == "up":
        s = 1
    else:
        s = 0
    goods_id = request.GET.get("goods_id")
    refer = request.META.get("HTTP_REFERER")  # 代表上一次的url
    if goods_id:
        goods = Goods.objects.filter(id=goods_id).first()
        goods.goods_status = s
        goods.save()
    return HttpResponseRedirect(refer)


def order_list(request):
    status = request.GET.get("status")

    store_id = request.COOKIES.get("has_store")
    store = Store.objects.filter(id=store_id).first()
    store_name = store.store_name
    order_list = OrderDetail.objects.filter(order_id__order_status=status, goods_store=store_name)
    return render(request, "store/order_list.html", locals())


def base(request):
    return render(request, "store/base.html", locals())


# api接口视图
# ViewSets define the view behavior

from rest_framework import viewsets
from Store.serializers import GoodsSerializer,GoodsTypeSerializer
from django_filters.rest_framework import DjangoFilterBackend #导入过滤器

class GoodsViewSet(viewsets.ModelViewSet):
    """查询所有商品 返回过滤的类"""
    queryset = Goods.objects.all()  # 具体返回的对象
    serializer_class = GoodsSerializer  # 指定过滤的类

    filter_backends = [DjangoFilterBackend] #指出采用的哪个过滤器
    filterset_fields = ['goods_name','goods_price'] #过滤查询的字段

class TypeViewSet(viewsets.ModelViewSet):
    """返回查询内容"""
    queryset = GoodsType.objects.all()
    serializer_class = GoodsTypeSerializer

from django.core.mail import send_mail
def sendMail(request):
    send_mail("邮件主题", "邮件内容", "from_email", ["to_email"], fail_silently=False)



#
# from CeleryTask.tasks import add
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
#
# def get_add(request):
#     add.delay(2, 3)
#     return JsonResponse({"statue": 200})
#
@cache_page(10*60)
def small_white_views(request):
    print("我是小白视图")
    # raise TypeError("我就不想好好的")
    return HttpResponse("我是小白视图")
#
# def small_white_views(request):
#     # print("我是小白视图")
#
#     rep = HttpResponse("I am rep")
#     rep.render = lambda: HttpResponse("hello world")
#     return rep
#
# # def small_white_views(request):
# #     # print("我是小白视图")
# #     def hello():
# #         return HttpResponse("hello world")
# #     rep = HttpResponse("I am rep")
# #     rep.render = hello
# #     return rep
#
# # def small_white_views(request):
# #     print("我是小白视图")
# #     def render():
# #         print("hello world")
# #         return HttpResponse("98k")
# #     rep = HttpResponse("od")
# #     rep.render = render
# #     return rep
