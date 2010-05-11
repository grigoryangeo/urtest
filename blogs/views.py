# File encoding: utf-8

# все ниже хрень

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import update_object, create_object
from django.http import Http404

from lib.helpers import render_to_request

from blogs.models import *

def blog_show(request, blog_id):
    """Блог
    
    Параметры:
        blog_id - ключ
    """
    blog = get_object_or_404(Blog, pk=blog_id)

    return render_to_request(request, 'blogs/blog_show.html', {'blog': blog})

    