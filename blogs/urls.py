from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

from django.conf.urls.defaults import *

from blogs.models import Blog, BlogEntry


urlpatterns = patterns('blogs.views',
    url(r'^(?P<blog_id>\d+)/(?P<entry_number>\d+)$', 'blog_show', name="blog_show"),
    url(r'wiki$', direct_to_template, {'template': 'blogs/wiki.html'},
        name="blog_wiki"),
    
)
