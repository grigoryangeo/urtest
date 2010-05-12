from django.contrib import admin
from urtest.blogs.models import Blog, BlogEntry

class BlogAdmin(admin.ModelAdmin):
    pass

class BlogEntryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogEntry, BlogEntryAdmin)
