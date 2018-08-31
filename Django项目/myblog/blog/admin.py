from django.contrib import admin
from .models import Category, Tag, Blog, Comment

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'content', 'pub')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'name', 'content', 'pub')


admin.site.site_header = '张全亮博客系统'
admin.site.site_title = '个人博客'