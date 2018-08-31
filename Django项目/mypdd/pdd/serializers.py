# -*- coding:utf-8 -*-
__author__ = '张全亮'
from rest_framework import serializers
from .models import Orderdown


class OrderdownSerializer(serializers.Serializer):   # 它序列化的方式很类似于Django的forms
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, max_length=50)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    token = serializers.CharField(required=False, max_length=255)
    goods_url = serializers.CharField(required=False, max_length=255)
    goods_number = serializers.IntegerField()
    orderno = serializers.CharField(max_length=50)
    notifyurl = serializers.CharField(max_length=255)
    sign = serializers.CharField(max_length=50)
    order = serializers.CharField(max_length=50, default='否')
    goods_id = serializers.CharField(max_length=50, default='')
    callbackurl = serializers.CharField(max_length=50, default='')
    extends = serializers.CharField(max_length=50, default='')

    def create(self, validated_data):
        """给定经验证的数据，创建并返回一个新的“摘录”实例。"""
        return Orderdown.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """给定已验证的数据，更新并返回现有的“摘录”实例"""
        instance.name = validated_data.get('name', instance.name)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.token = validated_data.get('token', instance.token)
        instance.goods_url = validated_data.get('goods_url', instance.goods_url)
        instance.goods_number = validated_data.get('goods_number', instance.goods_number)
        instance.orderno = validated_data.get('orderno', instance.orderno)
        instance.notifyurl = validated_data.get('notifyurl', instance.notifyurl)
        instance.sign = validated_data.get('sign', instance.sign)
        instance.order = validated_data.get('order', instance.order)
        instance.goods_id = validated_data.get('goods_id', instance.goods_id)
        instance.callbackurl = validated_data.get('callbackurl', instance.callbackurl)
        instance.extends = validated_data.get('extends', instance.extends)
        instance.save()
        return instance