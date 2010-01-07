# File encoding: utf-8

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from urtest.bugtracker.models import Bug, Project, Customer, PhysCustomer, UrCustomer, Tester

project_info = {
	"queryset": Project.objects.all(),
	"template_name": "project_list.html",
	"template_object_name": "project",
}

company_info = {
	"queryset": Customer.objects.all(),
	"template_name": "company_list.html",
        "template_object_name": "customer",
}

tester_info = {
	"queryset": Tester.objects.all(),
	"template_name": "tester_list.html",
	"template_object_name": "tester",
}

bug_info = {
    "queryset": Bug.objects.all(),
    "template_name": "bug_list.html",
    "template_object_name": "bug",
}

# Родные для сайта виды
# Импорт делается автоматически
urlpatterns = patterns('urtest.bugtracker.views',
    # Главная страница
    #(r'^$', direct_to_template, {'template': 'base.html'}),

    # Страницы для тестеров:
    (r'^testers/$', list_detail.object_list, tester_info),
    # Личная страница тестера
    (r'^testers/(\d+)(/[a-z]+)?$', 'tester_detail'),
    # Регистрация нового тестера
    (r'^testers/register$', 'tester_registraion'),

    # Страницы компаний:
    # Список всех компаний
    (r'^companies/$', list_detail.object_list, company_info),
    # Личная страница компании
    (r'^companies/(\d+)(/[a-z]+)?$', 'company_detail'),
    # Регистрация новой компании
    (r'^companies/register_f$', 'company_registraion', {'type': 'f'}),
    (r'^companies/register_y$', 'company_registraion', {'type': 'y'}),
(r'^projects/(\d+)/addbug$', 'add_bug'),
    # Страницы проектов:
    # Список всех проектов
    (r'^projects/$', list_detail.object_list, project_info),
    # Страница проекта
    (r'^projects/(\d+)(/[a-z]+)?$', 'project_detail'),
    # Добавление проекта
    (r'^projects/new$', 'new_project'),
    (r'^dogovor$', 'dogovor'),
    # Баги
    (r'^bugs/$', list_detail.object_list, bug_info),
    
    (r'^bugs/(\d+)$', list_detail.object_list, bug_info),
    # Example:
    # (r'^urtest/', include('urtest.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns += patterns('',
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

# XXX:
# Предпросмотр форм
# Заменяем ProjectForm на другое имя формы
from bugtracker.forms import *
urlpatterns += patterns('',
    (r'^formpreview$', StupidFormPreview(ProjectForm)),
)

urlpatterns += patterns('django.contrib.auth.views',
    # Авторизация
    (r'^$', 'login', {'template_name': 'main.html'}),
    # Выход
    (r'^logout$', 'logout', {'template_name': 'logout.html'}),
)

# Подгрузка JS для интернационализации
# Требуется для виджета с множественным выбором
urlpatterns += patterns('',
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
)

# Статические файлы: CSS и тд
urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
       {'document_root': 'media'}),

)
