# File encoding: utf-8

from django.contrib.auth.models import User
from django.contrib.auth import get_user, authenticate, login
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

import settings

from models import *
from forms import *
from helpers import *


def project_detail(request, id):
    """
    Детали проекта, вкладка с информацией
    """
    project = get_object_or_404(Project, pk=id)
    testers = project.testers.all()

    tester_in_project = request.user in testers

    return render_to_request(reguest, 'project_detail.html',
                             {'tester_in_project': tester_in_project,
                              'project': project,
                              'testers': testers})


def project_detail_testers(request, id):
    """
    Детали проекта, список тестеров
    """
    project = get_object_or_404(Project, pk=id)
    testers = project.testers.all()

    tester_in_project = request.user in testers

    return render_to_request(request, 'project_testers.html',
                             {'testers': testers,
                              'tester_in_project': tester_in_project,
                              'project': project})


def project_detail_bugs(request, id):
    """
    Детали проекта, вкладка со списком багов
    """
    project = get_object_or_404(Project, pk=id)
    testers = project.testers.all()
    bugs = project.bugs.all()

    tester_in_project = request.user in testers

    return render_to_request(request, 'project_bugs.html',
                             {'bugs': bugs,
                              'tester_in_project': tester_in_project,
                              'project': project})


@login_required
def project_add_tester(request, id):
    """
    Добавление авторизованного тестера к проекту
    """
    project = get_object_or_404(Project, pk=id)

    if not request.user.is_authenticated():
        raise PermissionDenied

    if not request.user == tester:
        raise PermissionDenied

    project.add_tester(request.user)
    return HttpResponseRedirect(reverse('project_detail_testers',
                                        (), {'id': id}))


@login_required
def project_add(request):
    """
    Добавление нового проекта
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return HttpResponseRedirect(project.get_absolute_url())
    else:
        form = ProjectForm()
    return render_to_request(request, 'new_project.html', {'form': form})


def project_add_bug(request, project_id):
    """
    Добавление бага в проект
    """
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(project.get_absolute_url())
    else:
        form = BugForm()
    return render_to_request(request, 'addbug.html',
            {'form': form, 'project_id': project_id})


@login_required
def bug_detail(request, id):
    """
    Детали бага
    """

    bug = get_object_or_404(Bug, pk=id)
    customer_own = request.user == bug.project.customer

    if request.method == 'POST':
        form = BugDetail(request.POST, instance=bug)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(bug.get_absolute_url())
    else:
        form = BugDetail(instance=bug)
    return render_to_request(request, 'bug_detail.html', locals())
