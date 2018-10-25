from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser
from .models import OrderdownSerializer, Orderdown, Order, OrderSerializer, Evaluate, EvaluateSerializer
from .forms import UserForm


# Create your views here.
def Orderdown_list(request):
    if request.method == 'GET':
        snippets = Orderdown.objects.all()
        orderdown = OrderdownSerializer(snippets, many=True)
        return JsonResponse(orderdown.data, safe=False)
        # result = {'code': 0, 'msg': '请求方式必须为POST', 'order_sn': '', 'pay_url': ''}
        # return JsonResponse(result)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print('data', data)
        orderdown = OrderdownSerializer(data=data)
        if orderdown.is_valid():
            orderdown.save()
            return JsonResponse(orderdown.data, status=201)
        return JsonResponse(orderdown.errors, status=400)


def Order_list(request):
    if request.method == 'GET':
        snippets = Order.objects.all()
        order = OrderSerializer(snippets, many=True)
        return JsonResponse(order.data, safe=False)
        # result = {'code': 0, 'msg': '请求方式必须为POST', 'order_sn': '', 'pay_url': ''}
        # return JsonResponse(result)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print('data', data)
        order = OrderSerializer(data=data)
        if order.is_valid():
            order.save()
            return JsonResponse(order.data, status=201)
        return JsonResponse(order.errors, status=400)


def Evaluate_list(request):
    if request.method == 'GET':
        snippets = Evaluate.objects.all()
        evaluate = EvaluateSerializer(snippets, many=True)
        return JsonResponse(evaluate.data, safe=False)
        # result = {'code': 0, 'msg': '请求方式必须为POST', 'order_sn': '', 'pay_url': ''}
        # return JsonResponse(result)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print('data', data)
        evaluate = EvaluateSerializer(data=data)
        if evaluate.is_valid():
            evaluate.save()
            return JsonResponse(evaluate.data, status=201)
        return JsonResponse(evaluate.errors, status=400)


# 注册
def register_view(request):
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():
            # 获取到表单信息
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 判断用户是否存在
            user = auth.authenticate(username=username, password=password)
            print('用户', user)
            if user:
                print('账号已存在，注册失败.')
                context['userExit'] = True
                return render(request, 'register.html', context=context)

            # 添加到数据库（还可以加一些字段的处理）
            user = User.objects.create_user(username, password)
            user.save()
            print('账号注册成功,  保存数据库')
            # 添加到session
            request.session['username'] = username

            # 调用auth登陆
            auth.login(request, user)

            # 重定向到首页
            return redirect('success.html')
    else:
        context = {'isLogin': False}
        # 将req 、页面 、以及context{}（要传入html文件中的内容包含在字典里）返回
    return render(request, 'register.html', context)


# 登陆
def login_view(request):
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # 获取表单用户名密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print('user', username, password)
            # 获取的表单数据与数据库进行比较
            user = authenticate(username=username, password=password)
            print('登陆', user)
            if user:
                auth.login(request, user)
                request.session['username'] = username
                return render(request, 'success.html')
            else:
                context = {'isLogin': False, 'pawd': False}
                return render(request, 'failure.html', context=context)
    else:
        context = {'isLogin': False, 'pswd': True}
    return render(request, 'login.html', context)


# 登出
def logout_view(request):
    # 清理cookie里保存username
    auth.logout(request)
    return redirect('/')
