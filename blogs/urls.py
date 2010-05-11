from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

from blogs.models import Blog, BlogMsg

from django.conf.urls.defaults import *

urlpatterns = patterns('blogs.views',
    url(r'^blogs/(?P<blog_id>\d+)$', 'blogs_show', name="blogs_show"),
)
