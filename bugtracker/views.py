# File encoding: utf-8

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from models import *
from forms import *


def add_bug(request):
    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bugs/')
    else:
        form = BugForm()
    return render_to_response('addbug.html',{'form': form},
                              context_instance=RequestContext(request))


# компании
def company_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if customer.type == 'f':
        template = 'PhysCustomer_detail.html'
    else:
        template = 'UrCustomer_detail.html'
    detail = customer.get_detail()
    fields = [(f.verbose_name, getattr(detail, f.name)) for f in detail._meta.fields[2:]]
    return render_to_response(template, {'fields': fields, 'detail': detail},
        context_instance=RequestContext(request))


def company_registraion(request, type):
    if type == 'y':
        form_type = UrCustomerForm
    elif type == 'f':
        form_type = PhysCustomerForm
    if request.method == 'POST':
        form = form_type(request.POST)
        if form.is_valid():
            ur_customer = form.save(commit=False)
            user = User()
            user.username = user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            customer = Customer.objects.create(type=type, user=user)
            ur_customer.customer = customer
            ur_customer.save()
            return HttpResponseRedirect('/')
    else:
        form = form_type()
    return render_to_response('company_registraion.html',{'form': form, 'type': type})
                              
# тестеры
def tester_registraion(request):
    if request.method == 'POST':
        form = TesterForm(request.POST)
        if form.is_valid():
            tester = Tester()
            user = User()
            user.username = user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            tester.user = user
            tester.surname = form.cleaned_data['last_name']
            tester.first_name = form.cleaned_data['first_name']
            tester.second_name = form.cleaned_data['second_name']
            tester.email = form.cleaned_data['email']
            tester.save()
            tester.osystems = form.cleaned_data['os']
            tester.program_languages = form.cleaned_data['program_languages']
            tester.testing_types = form.cleaned_data['testing_types']
            tester.browsers = form.cleaned_data['browsers']
            tester.save()
            return HttpResponseRedirect('/')
    else:
        form = TesterForm()
    return render_to_response('tester_registraion.html',{'form': form})

@login_required
def tester_detail(request, pk):
    try:
        tester = Tester.objects.get(pk=pk)
    except Tester.DoesNotExist:
        raise Http404
    projects = tester.projects.all()
    return render_to_response('tester_detail.html', locals(),
                              context_instance=RequestContext(request))


# проекты
#def new_project(request):
#    if request.method == 'POST':
#        form = ProjectForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect('/projects/')
#    else:
#        form = ProjectForm()
#    return render_to_response('new_project.html',{'form': form})

@login_required
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        raise Http404
    testers = project.testers.all()
    bugs = project.bugs.all()
    return render_to_response('project_detail.html', locals(),
                              context_instance=RequestContext(request))


