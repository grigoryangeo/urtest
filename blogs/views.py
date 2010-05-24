# File encoding: utf-8

from django.shortcuts import get_object_or_404

from lib.helpers import render_to_request
from django.shortcuts import get_object_or_404, redirect

from blogs.models import *
from blogs.forms import *
from bugtracker.models import Project

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

    # являемся ли мы хозяином блога
    viewing_self = request.user == blog.owner
    # являемся ли мы хозяином проекта, чей блог смотрим
    if isinstance(blog.owner, Project):
        viewing_self = request.user == blog.owner.customer
        

    if not viewing_self:
        return render_to_request(request, 'blogs/blog_show.html', {'blog': blog,
                'entries': entries, 'top': top, 'floor': floor,
                'number1': number, 'number2': entry_number_end})

    # добавление сообщения
    if request.method == 'POST':
        form = BlogEntryForm(request.POST)
        if form.is_valid():
            form.save(blog=blog)
            return redirect('blog_show', blog_id=blog_id, entry_number=0)
    else:
        form = BlogEntryForm()
                
    return render_to_request(request, 'blogs/blog_show.html', {'blog': blog,
                'entries': entries, 'top': top, 'floor': floor,
                'number1': number, 'number2': entry_number_end,
                'form': form })


