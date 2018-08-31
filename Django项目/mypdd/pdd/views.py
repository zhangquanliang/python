from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import OrderwownSerializer, Orderdown

# Create your views here.
def Orderdown_list(request):
    if request.method == 'GET':
        snippets = Orderdown.objects.all()
        orderdown = OrderwownSerializer(snippets, many=True)
        return JsonResponse(orderdown.data, safe=False)
        # result = {'code': 0, 'msg': '请求方式必须为POST', 'order_sn': '', 'pay_url': ''}
        # return JsonResponse(result)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print('data', data)
        orderdown = OrderwownSerializer(data=data)
        if orderdown.is_valid():
            orderdown.save()
            return JsonResponse(orderdown.data, status=201)
        return JsonResponse(orderdown.errors, status=400)