from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
#from django.views.generic.create_update import *

urlpatterns = patterns('bugtracker.views',
    (r'^projects/show/(?P<id>\d+)$', 'project_detail'),
    (r'^projects/show/(?P<id>\d+)/testers$', 'project_detail_testers'),
    (r'^projects/show/(?P<id>\d+)/bugs$', 'project_detail_bugs'),
    (r'^projects/enlist/(?P<id>\d+)$', 'project_add_tester'),
    (r'^projects/list$',direct_to_template, {'template': 'project_list.html'}),
    (r'^projects/add$', 'project_add'),
    (r'^projects/add_bug/(?P<project_id>\d+)$', 'project_add_bug'),

    (r'^bugs/show/(?P<id>\d+)$','bug_detail'),
    (r'^bugs/list$', direct_to_template, {'template': 'bug_list.html'}),
)
