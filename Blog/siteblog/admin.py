from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'created', 'status']
    list_filter = ['status', 'author', 'created', 'published']
    search_fields = ['title', 'content']
    raw_id_fields = ['author']
    date_hierarchy = 'published'
    readonly_fields = ['published', 'created', 'updated']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['status', 'published']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']