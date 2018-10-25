from django.shortcuts import render, render_to_response
from .models import *
from .forms import CommentForm
from django.http import Http404


# Create your views here.
def get_blogs(request):
    blogs = Blog.objects.all().order_by('-pub')  # 获取到所有的博客按时间倒序
    return render_to_response('login.html', context={'blogs': blogs})  # 传递context:blog参数到固定页面


def get_details(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)  # 获取固定的blog_id对象
    except Blog.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['blog'] = blog
            Comment.objects.create(**cleaned_data)
    ctx = {
        'blog': blog,
        'comments': blog.comment_set.all().order_by('-pub'),
        'form': form
    }  # 返回3个参数
    return render(request, 'register.html', context=ctx)
