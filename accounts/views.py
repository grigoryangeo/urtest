# File encoding: utf-8

from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from lib.helpers import render_to_request

from accounts.models import *
from accounts.forms import *


def tester_detail(request, id):
    """Детали тестера
    
    Параметры:
        id - ключ
    """
    tester = get_object_or_404(Tester, id=id)
    user = request.user

    viewing_self = user.tester == tester

    if not viewing_self:
        return render_to_request(request, 'accounts/tester_detail.html', {'tester': tester})

    if request.method == "POST":
        form = TesterChangeForm(request.POST, instance=tester)
        if form.is_valid():
            form.save()
    else:
        form = TesterChangeForm(instance=tester)
    return render_to_request(request, 'accounts/tester_detail.html', {'tester': tester, 'form': form})


def tester_detail_projects(request, id):
    """
    Детали тестера, вкладка со списком проектов тестера
    """
    tester = get_object_or_404(Tester, id=id)
    projects = tester.projects.all()
    return render_to_request(request, 'tester_detail_projects.html',
                             {'tester': tester, 'projects': projects})


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
        return render_to_request(request,'tester_registraion.html', {'reg_form': form})


def company_detail(request, id):
    """Детали компании
    
    Параметры:
        id - ключ
    """
    customer = get_object_or_404(Customer, id=id).detail

    if customer.type == 'p':
        template = 'PhysCustomer_detail.html'
    else:
        template = 'UrCustomer_detail.html'

    return render_to_request(request, template, {'customer': customer})


def company_detail_projects(request, id):
    """
    Детали компании, вкладка со списком проектов компании
    """
    customer = get_object_or_404(Customer, id=id)
    projects = customer.projects.all()
    return render_to_request(request, 'customer_project_detail.html',
                             {'projects': projects, 'customer': customer})


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
    return render_to_request(request,'company_registraion.html',{'reg_form': form, 'type': type})


def redirect_to_self(request):
    """Переадресация в свой личный кабинет"""
    # Получение текущего пользователя
    user = request.user

    # Переход на админку для админа
    if user.is_superuser:
        return HttpResponseRedirect('/admin')

    # Переход в личный кабинет для тестера/компании
    if isinstance(user, Customer) or isinstance(user, Tester):
        return HttpResponseRedirect(user.get_absolute_url())

    # Не админ, не нормальный пользователь --- кабинета нет, 404
    raise Http404
