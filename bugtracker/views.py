# File encoding: utf-8

from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from models import *
from forms import *


# компании
def company_detail(request, pk, page=''):
     print pk, page
     customer = get_object_or_404(Customer, pk=pk)
     if page == None:
        if customer.type == 'f':
           template = 'PhysCustomer_detail.html'
        else:
           template = 'UrCustomer_detail.html'
        detail = customer.get_detail()
        projects=  customer.projects.all()
        fields = [(f.verbose_name, getattr(detail, f.name)) for f in detail._meta.fields[2:]]
        return render_to_response(template, {'fields': fields, 'detail': detail,'projects':projects},
        context_instance=RequestContext(request))
     elif page == '/projects':
        projects=  customer.projects.all()
        return render_to_response('customer_project_detail.html',{'projects':projects},
            context_instance=RequestContext(request))
     else:
        raise Http404


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
            form.save_m2m()
            return HttpResponseRedirect('/thanks')
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
            tester.description = form.cleaned_data['description']
            tester.save()
            tester.osystems = form.cleaned_data['os']
            tester.program_languages = form.cleaned_data['program_languages']
            tester.testing_types = form.cleaned_data['testing_types']
            tester.browsers = form.cleaned_data['browsers']
            tester.save()
            return HttpResponseRedirect('/thanks')
    else:
        form = TesterForm()
    return render_to_response('tester_registraion.html',{'form': form})


def tester_detail(request, pk, page=''):
    print pk, page
    tester = get_object_or_404(Tester, pk=pk)
    if page == None:
        fields = [(f.verbose_name, getattr(tester, f.name)) for f in tester._meta.fields[2:]]
        return render_to_response('tester_detail.html', locals(),
                              context_instance=RequestContext(request))
    elif page == '/projects':
        projects = tester.projects.all()
        return render_to_response('tester_detail_projects.html', locals(),
            context_instance=RequestContext(request))
    else:
        raise Http404

def dogovor(request):
    return render_to_response('dogovor.html', context_instance=RequestContext(request))

def thanks(request):
    return render_to_response('thanks.html', context_instance=RequestContext(request))

# проекты
def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.customer = get_user(request).customer
            project.save()
	    form.save_m2m()
            return HttpResponseRedirect('/projects/')
    else:
        form = ProjectForm()
    return render_to_response('new_project.html',{'form': form},
        context_instance=RequestContext(request))


def project_detail(request, pk, page=''):
    print pk, page
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        raise Http404
    testers = project.testers.all()
    bugs = project.bugs.all()
    if page == None:
       return render_to_response('project_detail.html', locals(),
                              context_instance=RequestContext(request))
    elif page == '/bugs':
        return render_to_response('project_bugs.html', locals(),
            context_instance=RequestContext(request))
    elif page == '/testers':
        return render_to_response('project_testers.html', locals(),
            context_instance=RequestContext(request))
    else:
        raise Http404

# баги
def bug_list(request):
    return render_to_response('bug_list.html')

def bug_details(request, pk, page, bk):
    try:
        bugs = Bug.objects.get(pk=bk)
    except Bug.DoesNotExist:
        raise Http404
    if page == '/bugs/':
        pk = int(pk)
        severity = bugs.get_severity_display()
        status = bugs.get_status_display()
        return render_to_response('bug_detail.html',locals(),
            context_instance=RequestContext(request))
    else:
        raise Http404

def add_bug(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.project = project
            bug.tester = get_user(request).tester
            bug.save()
            return HttpResponseRedirect('/projects/%s' % project_pk)
    else:
        form = BugForm()
    return render_to_response('addbug.html',{'form': form},
                              context_instance=RequestContext(request))

