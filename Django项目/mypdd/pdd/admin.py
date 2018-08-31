from django.contrib import admin
# from .models import Orderdown, Order
from .models import Orderdown, Order, Evaluate

# Register your models here.
@admin.register(Orderdown)
class OrderdownAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'goods_number', 'orderno', 'order', 'create_date')
    list_display_links = ('name', 'amount', 'orderno', 'order')
    ordering = ('id',)  # 排序字典，-未降序排序

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'orderno', 'order_sn', 'amount', 'status', 'evalute', 'create_date', 'update_date')
    list_display_links = ('orderno', 'order_sn', 'evalute')
    list_editable = ['name', 'status']
    search_fields = ['name', 'orderno', 'order_sn']
    ordering = ('id',)  # 排序字典，-未降序排序

@admin.register(Evaluate)
class EvaluateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order_sn', 'content', 'over', 'create_date')
    list_display_links = ('name', 'order_sn', 'over')
    ordering = ('id',)  # 排序字典，-未降序排序


admin.site.site_header = '拼多多后台管理系统'
admin.site.site_title = '管理系统'