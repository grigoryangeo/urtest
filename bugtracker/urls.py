from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
#from django.views.generic.create_update import *

from django.views.generic import list_detail


project_info = {
"queryset": Project.objects.all(),
"template_name": "project_list.html",
"template_object_name": "project",
}

bug_info = {
    "queryset": Bug.objects.all(),
    "template_name": "bug_list.html",
    "template_object_name": "bug",
}

urlpatterns = patterns('bugtracker.views',
    (r'^projects/show/(?P<id>\d+)$', 'project_detail'),
    (r'^projects/show/(?P<id>\d+)/testers$', 'project_detail_testers'),
    (r'^projects/show/(?P<id>\d+)/bugs$', 'project_detail_bugs'),
    (r'^projects/enlist/(?P<id>\d+)$', 'project_add_tester'),
    (r'^projects/list$',list_detail.object_list, project_info),),
    (r'^projects/add$', 'project_add'),
    (r'^projects/add_bug/(?P<project_id>\d+)$', 'project_add_bug'),

    (r'^bugs/show/(?P<id>\d+)$','bug_detail'),
    (r'^bugs/list$', list_detail.object_list, bug_info),
)
