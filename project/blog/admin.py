from django.contrib import admin
from .models import Category, Article, Comment, Profile


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'views', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    list_editable = ['views']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    List_display = ['category', 'title', 'id', 'user', 'text']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)



