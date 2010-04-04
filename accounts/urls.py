from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

from accounts.models import Tester, Customer

from django.conf.urls.defaults import *

tester_dict = {
    'queryset': Tester.objects.all,
    'template_object_name': 'tester'
}

customer_dict = {
    'queryset': Customer.objects.all,
    'template_object_name': 'customer'
}

urlpatterns = patterns('accounts.views',
    (r'^testers/show/(?P<id>\d+)$', 'tester_detail'),
    (r'^testers/show/(?P<id>\d+)/projects$', 'tester_detail_projects'),
    (r'^testers/list', object_list, tester_dict),
    (r'^testers/register', 'tester_registration'),

    (r'^companies/show/(?P<id>\d+)$', 'company_detail'),
    (r'^companies/show/(?P<id>\d+)/projects$', 'company_detail_projects'),
    (r'^companies/list$', object_list, tester_dict),
    (r'^companies/register_(?P<id>[jp])$', 'company_registration'),

    (r'thanks$', direct_to_template, {'template': 'accounts/thanks.html'}),

    (r'^me$', 'redirect_to_self'),
)
