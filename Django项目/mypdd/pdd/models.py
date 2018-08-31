from django.db import models
from rest_framework import serializers

# Create your models here.
class Orderdown(models.Model):
    name = models.CharField('用户', max_length=50)
    amount = models.DecimalField('金额', max_digits=20, decimal_places=2)
    token = models.CharField('通讯令牌', max_length=255)
    goods_url = models.CharField('商品地址', max_length=255)
    goods_number = models.IntegerField('商品数量')
    orderno = models.CharField('己方订单号', max_length=50, unique=True)
    notifyurl = models.CharField('回调地址', max_length=255)
    sign = models.CharField('签名', max_length=50)
    order = models.CharField('是否已提交订单', max_length=50, blank=True, null=True, default='否')
    goods_id = models.CharField('商品ID', blank=True, default='', max_length=50)
    callbackurl = models.CharField('回调', blank=True, default='', max_length=50)
    extends = models.CharField('扩展字段', blank=True, default='', max_length=50)
    create_date = models.DateTimeField('创建日期', auto_now_add=True)
    class Meta:
        verbose_name = '我的下单'
        verbose_name_plural =verbose_name
    def __str__(self):
        return self.name


class OrderwownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderdown
        fields = ('id', 'name', 'amount', 'token', 'goods_url', 'goods_number', 'orderno', 'notifyurl', 'sign',
                  'order', 'goods_id', 'callbackurl', 'extends')


class Order(models.Model):
    name = models.CharField('用户', max_length=50)
    orderno = models.CharField('己方订单号', max_length=50, unique=True)
    order_sn = models.CharField('订单编号', max_length=50, unique=True)
    amount = models.DecimalField('订单金额', max_digits=20, decimal_places=2)
    order_type = models.CharField('订单类型', max_length=50)
    pay_url = models.CharField('付款链接', max_length=50)
    status = models.CharField('订单状态', max_length=50)
    evalute = models.CharField('是否已评价', max_length=50, blank=True, null=True, default='否')
    create_date = models.DateTimeField('创建日期')
    update_date = models.DateTimeField('更新日期', auto_now_add=True)
    class Meta:
        verbose_name = '我的订单'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Evaluate(models.Model):
    name = models.CharField('用户', max_length=50)
    goods_id = models.CharField('商品ID', max_length=50)
    goods_url = models.CharField('商品地址', max_length=255)
    order_sn = models.CharField('订单编号', max_length=50, unique=True)
    content = models.TextField('评价内容', blank=True, null=True, default='')
    over = models.CharField('是否完结订单', max_length=50, blank=True, null=True, default='是')
    create_date = models.DateTimeField('创建日期', blank=True, auto_now_add=True)
    class Meta:
        verbose_name = '我的评价'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name