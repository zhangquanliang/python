from django.db import models

# Create your models here.
class Category(models.Model):
    """博客分类"""
    name = models.CharField('名称', max_length=30)
    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField('名称', max_length=16)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField('标题', max_length=32)
    author = models.CharField('作者', max_length=16)
    content = models.TextField('内容', default='')
    pub = models.DateField('发布时间', auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name='分类') # 多对一(博客--类别)
    tag = models.ManyToManyField(Tag, verbose_name='标签')  # 多对多
    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, verbose_name='博客')  #(博客--评论:一对多)
    name = models.CharField('称呼', max_length=16)
    email = models.EmailField('邮箱')
    content = models.TextField('内容', max_length=240, default='')
    pub = models.DateField('发布时间', auto_now_add=True)
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.content
