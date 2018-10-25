# -*- coding:utf-8 -*-
__author__ = '张全亮'
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)