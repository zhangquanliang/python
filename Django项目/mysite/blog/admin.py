from django.contrib import admin
from .models import Article, Tags, Category

# Register your models here.
admin.site.register(Tags)
# admin.site.register(Article)
admin.site.register(Category)


"""管理应用注册方式"""
# 1 装饰器注册
# @admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'body', 'riqi') # 可以看见的信息
    list_per_page = 20  # 每页显示的记录，默认100
    ordering = ('-id', )    # 排序字典，-未降序排序
    list_editable = ['user']   # 设置可编辑字典，在列表里编辑
    list_display_links = ('id', 'title')   # 设置哪些字段可以点击进入编辑界面
    actions_on_top = True   # 操作选项，默认为True，为顶部
    actions_on_bottom = False  # 默认False
    search_fields = ['title']   # 搜索框
    list_filter = ['user']    # 右侧栏过滤器，按作者进行筛选
    date_hierarchy = 'created_time'  # 日期筛选属性

admin.site.site_header = '张全亮个人系统'  # 修改头部信息
admin.site.site_title = '独家页面'  # 修改标签页


# 2 注册参数
admin.site.register(Article, ArticleAdmin)