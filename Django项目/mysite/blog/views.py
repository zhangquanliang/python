from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog import models

def test(request):
    return HttpResponse('Success')

# Create your views here.
def Pay(request):
    pay_url = 'weixin://wap/pay?prepayid%3Dwx22104238275891644864c8980927934563&package=2815091138&noncestr=1534905758&sign=6f72c10acf8350cdce132b56f5cfee3a'
    pay_dict = {
        'pay_url1': pay_url
    }
    return render(request, 'pay.html', context=pay_dict)


def Index(request):
    if request.method == 'POST':
        print('post', request.POST)
    else:
        # return redirect('http://www.baidu.com', permanent=True)   # True为永久重定向到目标网址
        # return redirect('/pay', permanent=True)
        print('GET', request.GET)
    blog_index = models.Article.objects.all().order_by('id')
    context = {
        "blog_index": blog_index
    }
    return render(request, 'index.html', context=context)

def orm(request):
    # 第一种方法：
    # models.Article.objects.create(title='增加标题一', category_id=3, body='增加内容一', user_id=1)
    # 第二种方法：添加数据，实例化表类，在实例化里传参为字段和值
    obj = models.Article(title='增加标题二', category_id=4, body='增加内容二', user_id=1)
    # 写入数据库
    obj.save()
    # 第三种方法：将要写入的数据组合成字典，键为字段值为数据
    dic = {'title': '增加标题三', 'category_id': '4', 'body': '增加内容三', 'user_id': '1'}
    # 添加到数据库，注意字典变量名称一定要加**
    models.Article.objects.create(**dic)

    """删除"""
    # models.Article.objects.filter(id=3).delete()

    """更改"""
    models.Article.objects.filter(id=6).update(intro='123')
    return HttpResponse('orm')