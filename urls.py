# File encoding: utf-8

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('bugtracker.views',
    # Главная страница
    (r'^$', direct_to_template, {'template': 'main.html'}),

    # Учетные записи, регистрация и тд
    (r'^accounts/', include('urtest.accounts.urls')),
    
    # Проекты, баги
    (r'^bugtracker/', include('urtest.bugtracker.urls')),

    # Админка
    (r'^admin/', include(admin.site.urls)),
)

# Вход/выход
urlpatterns += patterns('django.contrib.auth.views',
    # Авторизация
    (r'^login$', 'login', {'template_name': 'login.html'}),
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
