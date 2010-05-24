# File encoding: utf-8

from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

import settings

from models import Bug, Project
from forms import *
from lib.helpers import render_to_request


def handle_uploaded_file(f, s):
    destination = open('upload/%s_%s' % (s, f.name), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def project_detail(request, project_id):
    """
    Детали проекта, вкладка с информацией
    """
    project = get_object_or_404(Project, pk=project_id)
    testers = project.testers.all()
    user = request.user
    
    user_can_enlist = user.is_authenticated() and user.is_tester() and \
            user not in testers

    return render_to_request(request, 'bugtracker/project_detail.html',
                             {'user_can_enlist': user_can_enlist,
                              'project': project
                             })


def project_detail_testers(request, project_id):
    """
    Детали проекта, список тестеров
    """
    project = get_object_or_404(Project, pk=project_id)
    testers = project.testers.all()

    return render_to_request(request, 'bugtracker/project_detail_testers.html',
                             {'testers': testers,
                              'project': project})


def project_detail_bugs(request, project_id):
    """
    Детали проекта, вкладка со списком багов
    """
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    testers = project.testers.all()
    bugs = project.bugs.all()

    user_can_add_bug = user in testers

    return render_to_request(request, 'bugtracker/project_detail_bugs.html',
                             {'bugs': bugs,
                              'project': project,
                              'user_can_add_bug': user_can_add_bug,
                             })


@login_required
def project_add_tester(request, project_id):
    """
    Добавление авторизованного тестера к проекту
    """
    project = get_object_or_404(Project, pk=project_id)

    if not request.user.is_tester():
        raise PermissionDenied

    project.add_tester(request.user)

    return redirect('project_detail_testers', project_id=project.pk)


@login_required
def project_add(request):
    """
    Добавление нового проекта
    """
    # Пользователь должен быть заказчиком
    user = request.user
    if not user.is_customer():
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(customer=user, f=request.FILES['file'])
            str = "%s" % (project.pk)
            handle_uploaded_file(request.FILES['file'], str)
            return redirect(project)
    else:
        form = ProjectForm()
    return render_to_request(request, 'bugtracker/project_add.html',
                             {'form': form})


@login_required
def project_add_bug(request, project_id):
    """
    Добавление бага в проект
    """
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    
    if request.method == 'POST':
        form = BugForm(request.POST, request.FILES)
        if form.is_valid():
            bug = form.save(tester=user, project=project, f=request.FILES['file'])
            str = "%s_%s" % (bug.project.pk, bug.pk)
            handle_uploaded_file(request.FILES['file'], str)
            return redirect(bug)
    else:
        form = BugForm()
    return render_to_request(request, 'bugtracker/project_add_bug.html',
            {'form': form, 'project': project})


@login_required
def bug_detail(request, bug_id):
    """
    Детали бага
    """

    bug = get_object_or_404(Bug, pk=bug_id)
    project=bug.project
    user_is_owner = request.user == bug.project.customer

    if not user_is_owner:
        return render_to_request(request, 'bugtracker/bug_detail.html',
                                {'bug': bug, 'project':project})

    if request.method == 'POST':
        form = BugStatusUpdateForm(request.POST, instance=bug)
        if form.is_valid():
            form.save()
            return redirect(request.user)
    else:
        form = BugStatusUpdateForm(instance=bug)
    return render_to_request(request, 'bugtracker/bug_detail.html',
                             {'bug': bug,
                              'form':form, 'project':project
                             })

