from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    """
        Django 要求模型必须继承 models.Model 类。
        Category 只需要一个简单的分类名 name 就可以了。
        CharField 指定了分类名 name 的数据类型，CharField 是字符型，
        CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
        然后给name设置了一个'分类'的名称
        """
    name = models.CharField('分类', max_length=100)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Tags(models.Model):
    """
        标签 Tag 也比较简单，和 Category 一样。
        再次强调一定要继承 models.Model 类！
        """
    name = models.CharField('标签', max_length=100)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


# Create your models here.
class Article(models.Model):
    title = models.CharField('标题', max_length=80)
    intro = models.TextField('内容', max_length=400, blank=True)  # blank=True允许为空

    # 文章分类，我们还使用了on_delete参数，这个是Django2.0强制ForeignKey必须使用的。
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类', default='1')

    # ManyToManyField，表明这是多对多的关联关系。
    tags = models.ManyToManyField(Tags, blank=True)
    body = models.TextField()

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField('发布时间', auto_now_add=True)

    def riqi(self):
        return self.created_time.strftime("%b %d %Y %H:%M:%S")
    riqi.short_description = '发布日期'  # 设置方法字段在admin中显示的标题
    riqi.admin_order_field = 'created_time' # 指定排序依据

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title