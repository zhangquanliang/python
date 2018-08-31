# -*- coding:utf-8 -*-
__author__ = '张全亮'
from rest_framework import serializers
from .models import *

class SnippetSerializer(serializers.Serializer):   # 它序列化的方式很类似于Django的forms
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})  # style的设置等同于Django的widget=widgets.Textarea
    linenos = serializers.CharField(required=False) # 用于对浏览器上的显示
    language = serializers.CharField(default='python',max_length=100)
    style = serializers.CharField(max_length=100, default='friendly')

    def create(self, validated_data):
        """给定经验证的数据，创建并返回一个新的“摘录”实例。"""
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """给定已验证的数据，更新并返回现有的“摘录”实例"""
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance