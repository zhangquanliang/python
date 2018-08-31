# -*- coding:utf-8 -*-
__author__ = '张全亮'
from django.conf.urls import url
from snippets import views

urlpatterns = [
    url(r'^api/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]