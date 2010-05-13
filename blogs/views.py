# File encoding: utf-8

from django.shortcuts import get_object_or_404

from lib.helpers import render_to_request
from django.shortcuts import get_object_or_404, redirect

from blogs.models import *
from blogs.forms import *

def blog_show(request, blog_id, entry_number):
    """
    Главная страница блога, со списком сообщений
    
    Параметры:
        blog_id - ключ
    """
    blog = get_object_or_404(Blog, pk=blog_id)

    # узнаем кол-во сообщений
    entries=blog.entries.all()
    number_of_entries = entries.count()

    # получаем номер соощения c конца
    entry_number_begin = int(entry_number)

    # узнаем номер сообщения 5 штук назад
    entry_number_end = entry_number_begin+5

    # получаем 5 сообщений до указханного
    entries = blog.entries.all().order_by('-pk')[entry_number_begin:entry_number_end]

    # еслть ли сообщения после
    top = False
    if (entry_number_begin > 0):
        top = True

    # есть ли сообщения до
    floor = False
    if (entry_number_end < number_of_entries):
        floor = True

    # расчет номера сообщения 5 штук вперед
    number = 0
    if entry_number_begin > 5:
        number = entry_number_begin-5

    # являемся ли мы хозяином
    viewing_self = request.user == blog.owner

    if not viewing_self:
        return render_to_request(request, 'blogs/blog_show.html', {'blog': blog,
                'entries': entries, 'top': top, 'floor': floor,
                'number1': number, 'number2': entry_number_end})
                
    return render_to_request(request, 'blogs/blog_show.html', {'blog': blog,
                'entries': entries, 'top': top, 'floor': floor,
                'number1': number, 'number2': entry_number_end,
                'form': BlogEntryForm() })


def add_entry(request, blog_id):
    """Добавление сообщения"""
    
    blog = get_object_or_404(Blog, pk=blog_id)

    if request.method == 'POST':
        form = BlogEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(blog=blog)
            return blog_show(request, blog_id, 0)
    else:
        form = BlogEntryForm()
    return blog_show

    