# -*- coding:utf-8 -*-
__author__ = '张全亮'
from rest_framework import serializers
from .models import Orderdown, Order, Evaluate


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


class OrderSerializer(serializers.Serializer):   # 它序列化的方式很类似于Django的forms
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, max_length=50)
    orderno = serializers.CharField(required=False, max_length=50)
    order_sn = serializers.CharField(required=False, max_length=50)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    order_type = serializers.CharField(required=False, max_length=50)
    pay_url = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=50)
    evalute = serializers.CharField(max_length=50, default='')

    def create(self, validated_data):
        """给定经验证的数据，创建并返回一个新的“摘录”实例。"""
        return Orderdown.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """给定已验证的数据，更新并返回现有的“摘录”实例"""
        instance.name = validated_data.get('name', instance.name)
        instance.orderno = validated_data.get('orderno', instance.orderno)
        instance.order_sn = validated_data.get('order_sn', instance.order_sn)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.order_type = validated_data.get('order_type', instance.order_type)
        instance.pay_url = validated_data.get('pay_url', instance.pay_url)
        instance.status = validated_data.get('status', instance.status)
        instance.evalute = validated_data.get('evalute', instance.evalute)
        instance.save()
        return instance


class EvaluteSerializer(serializers.Serializer):   # 它序列化的方式很类似于Django的forms
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, max_length=50)
    goods_id = serializers.CharField(required=False, max_length=50)
    goods_url = serializers.CharField(required=False, max_length=255)
    order_sn = serializers.CharField(required=False, max_length=50)
    content = serializers.CharField(required=False, max_length=1024)
    over = serializers.CharField(max_length=50)

    def create(self, validated_data):
        """给定经验证的数据，创建并返回一个新的“摘录”实例。"""
        return Orderdown.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """给定已验证的数据，更新并返回现有的“摘录”实例"""
        instance.name = validated_data.get('name', instance.name)
        instance.goods_id = validated_data.get('goods_id', instance.goods_id)
        instance.goods_url = validated_data.get('goods_url', instance.goods_url)
        instance.order_sn = validated_data.get('order_sn', instance.order_sn)
        instance.content = validated_data.get('content', instance.content)
        instance.over = validated_data.get('over', instance.over)
        instance.save()
        return instance