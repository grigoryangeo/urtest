# File encoding: utf-8

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import update_object, create_object
from django.http import Http404

from lib.helpers import render_to_request

from blogs.models import *

def blog_show(request, blog_id, entry_number):
    """
    Главная страница блога, со списком сообщений
    
    Параметры:
        blog_id - ключ
    """
    blog = get_object_or_404(Blog, pk=blog_id)

    entries=blog.entries.all()
    number_of_entries = entries.count()

    entry_number_end = int(entry_number)

    entry_number_begin = 0
    if entry_number_end >= 5:
        entry_number_begin = entry_number_end-5
        
        
    entries = blog.entries.all()[entry_number_begin:entry_number_end]


    top = False
    if (entry_number_end < number_of_entries):
        top = True
        
    floor = False
    if (entry_number_begin > 0):
        floor = True

    return render_to_request(request, 'blogs/blog_show.html', {'blog': blog,
                'entries': entries, 'top': top, 'floor': floor, 'number': entry_number_end})

    