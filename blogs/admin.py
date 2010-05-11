from django.contrib import admin
from urtest.blogs.models import Blog, BlogMsg

class BlogAdmin(admin.ModelAdmin):
    pass

class BlogMsgAdmin(admin.ModelAdmin):
    pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogMsg, BlogMsgAdmin)