from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    (r'^testers/show/(?P<id>\d+)$', 'tester_detail'),
    (r'^testers/show/(?P<id>\d+)/projects$', 'tester_detail_projects'),
    (r'^testers/list', 'tester_list'),
    (r'^testers/register', 'tester_registration'),

    (r'^companies/show/(?P<id>\d+)$', 'company_detail'),
    (r'^companies/show/(?P<id>\d+)/projects$', 'company_detail_projects'),
    (r'^companies/list', 'company_list'),
    (r'^companies/register', 'company_registration'),

    (r'^me', 'redirect_to_self'),
)
