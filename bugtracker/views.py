# File encoding: utf-8

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from models import Bug, Customer, PhysCustomer, UrCustomer, Project, Tester
from forms import BugForm, ProjectForm, TesterForm

#  те кто занимаются формами .это надо удалить
def bugs_list(request):
    bugs = Bug.objects.all()
    return render_to_response('buglist.html', {'bugs': bugs},
                              context_instance=RequestContext(request))


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
#def company_registraion(request):
#    if request.method == 'POST':
#        form = CompanyForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect('/companies/')
#    else:
#        form = CompanyForm()
#    return render_to_response('company_registraion.html',{'form': form})

#@login_required
#def company_detail(request, pk):
#    try:
#        company = Company.objects.get(pk=pk)
#    except Company.DoesNotExist:
#        raise Http404
#    projects = company.projects.all()
#    return render_to_response('company_detail.html', locals(),
#                              context_instance=RequestContext(request))

                              
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


