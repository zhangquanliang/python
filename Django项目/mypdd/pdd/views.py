from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import OrderdownSerializer, Orderdown, Order, OrderSerializer, Evaluate, EvaluateSerializer


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
