from django.db import models
from pygments.lexers import get_all_lexers   # 一个实现代码高亮的模块
from pygments.styles import get_all_styles
from .serializers import *

# LEXERS = [item for item in get_all_lexers() if item[1]]
# LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])  # 得到所有编程语言的选项
# STYLE_CHOICES = sorted((item, item) for item in get_all_styles())  # 列出所有配色风格


# Create your models here.
class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.CharField(default=False, max_length=100, blank=True, null=True)
    language = models.CharField(default='python', max_length=100)
    style = models.CharField(default='friendly', max_length=100)
    class Meta:
        ordering = ('created', )
class SnippetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'lineons', 'language', 'style')