# Serializers define the API representation.
from rest_framework import serializers
from Store.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """声明数据"""
    class Meta: #元类
        model = Goods  #进行接口序列化的模型
        fields = ['goods_name','goods_price','goods_number','goods_description']
        #序列要返回的字段


class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodsType
        fields = ['name', 'description']