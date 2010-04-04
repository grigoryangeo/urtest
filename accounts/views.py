# File encoding: utf-8

from django.contrib.auth.models import User
from django.contrib.auth import get_user, authenticate, login
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

import settings

from models import *
from forms import *

def tester_detail(request, id):
    """Детали тестера
    
    Параметры:
        id - ключ
    """
    tester = get_object_or_404(Tester, id=id)
    user = get_user(request)
    viewing_self = hasattr(user, 'tester') and user.tester == tester
    if viewing_self:
        if request.method == "POST":
            form = TesterDetailForm(request.POST, instance=tester)
            if form.is_valid():
                form.save()
        else:
            form = TesterDetailForm(instance=tester)
        return render_to_request(request, 'tester_detail.html', {'tester': tester, 'form':form},
            context_instance=RequestContext(request))
    else:
        return render_to_request(request, 'tester_detail.html', {'tester':tester})

def tester_edit(request, id):
    """
    Редактирование своих деталей тестером
    """
    if request.method == 'POST':
        form = TesterChangeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TesterChangeForm()
    return render_to_response('tester_detail.html',{'form': form})

def tester_detail_projects(request, id):
    """
    Детали тестера, вкладка со списком проектов тестера
    """
    tester = get_object_or_404(Tester, id=id)
    projects = tester.projects.all()
    return render_to_request(request, 'tester_detail_projects.html', {'tester': tester, 'projects':projects})

def tester_list(request):
    """Список тестеров"""
    return render_to_response('tester_list.html')

def tester_registration(request):
    """Регистрация тестера"""
    if request.method == 'POST':
        form = TesterRegForm(request.POST)
        if form.is_valid():
            form.save()
            send_activation_mail("%s %s" % (tester.surname, tester.first_name), user)
            return HttpResponseRedirect('/accounts/thanks')
    else:
        form = TesterRegForm()
    return render_to_response('tester_registraion.html',{'reg_form': form})

def company_detail(request, id):
    """Детали компании
    
    Параметры:
        id - ключ
    """
    customer = get_object_or_404(Customer, id=id)
    if customer.type == 'f':
        template = 'PhysCustomer_detail.html'
    else:
        template = 'UrCustomer_detail.html'
    detail = customer.get_detail()
    projects=  customer.projects.all()
    fields = [(f.verbose_name, getattr(detail, f.name)) for f in detail._meta.fields[2:]]
    return render_to_response(template, {'fields':fields, 'detail':detail, 'projects':projects, 'customer':customer},
    context_instance=RequestContext(request))

def company_detail_projects(request, id):
    """
    Детали компании, вкладка со списком проектов компании
    """
    customer = get_object_or_404(Customer, id=id)
    projects=  customer.projects.all()
    return render_to_response('customer_project_detail.html',{'projects':projects, 'customer':customer},
    context_instance=RequestContext(request))

def company_registration(request, type):
    """Детали компании

    Параметры:
        type - j либо p, Физ/Юр лицо
    """
    if type == 'y':
        form_type = JurCustomerRegForm
    elif type == 'f':
        form_type = PhysCustomerRegForm
    if request.method == 'POST':
        form = form_type(request.POST)
        if form.is_valid():
            form.save()
            send_activation_mail(customer.name, user)
            return HttpResponseRedirect('/accounts/thanks')
    else:
        form = form_type()
    return render_to_response('company_registraion.html',{'reg_form': form, 'type': type})

def company_list(request):
    """Список компаний"""
    return render_to_response('company_list.html')

def thanks(request):
    """Спасибо за регистрацию"""
    return render_to_response('thanks.html', context_instance=RequestContext(request))
    
def redirect_to_self(request):
    """Переадресация в свой личный кабинет"""
    # Получение текущего пользователя
    user = request.user
    # Переход на админку для админа
    if user.is_superuser:
        return HttpResponseRedirect('/admin')
    # Переход в личный кабинет для тестера/компании
    if hasattr(user, 'tester'):
        return HttpResponseRedirect('/accounts/testers/%s' % user.tester.pk)
    if hasattr(user, 'customer'):
        return HttpResponseRedirect('/accounts/companies/%s' % user.customer.pk)
    raise Http404
