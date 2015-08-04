from django.contrib import admin
from models import Blog, Category, Comment, Userprofile, Friend


class CategoryAdmin(admin.ModelAdmin):
    fields = ['title']


class BlogAdmin(admin.ModelAdmin):
    fields = ['title', 'body', 'pub_date', 'image', ]


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Userprofile)
admin.site.register(Friend)
