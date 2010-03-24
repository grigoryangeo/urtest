# File encoding: utf-8
from models import *
from forms import *
from helpers import *

def project_detail(request, id):
    """
    Детали проекта, вкладка с информацией
    """
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        raise Http404
    testers = project.testers.all()

    if request.user.is_authenticated():
        for tester in testers :
            if( tester.user == request.user ):
                project_tester = tester.user

    return render_to_response('project_detail.html', locals(),
                              context_instance=RequestContext(request))

def project_detail_testers(request, id):
    """
    Детали проекта, вкладка со списком тестеров
    """
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        raise Http404
    testers = project.testers.all()

    if request.user.is_authenticated():
        for tester in testers :
            if( tester.user == request.user ):
                project_tester = tester.user

    return render_to_response('project_testers.html', locals(),
            context_instance=RequestContext(request))

def project_detail_bugs(request, id):
    """
    Детали проекта, вкладка со списком багов
    """
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        raise Http404
    testers = project.testers.all()
    bugs = project.bugs.all()

    if request.user.is_authenticated():
        for tester in testers :
            if( tester.user == request.user ):
                project_tester = tester.user

    return render_to_response('project_bugs.html', locals(),
            context_instance=RequestContext(request))

def project_add_tester(request, id):
    """
    Добавление авторизованного тестера к проекту
    """
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        raise Http404
    
    user = request.user
    if not user.is_authenticated():
        raise PermissionDenied
    # Текущий залогиненый пользователь должен быть тестером
    if not hasattr(user, 'tester'):
        raise PermissionDenied
    tester = user.tester
    project.add_tester(tester)
    return HttpResponseRedirect('projects/show/%i/testers' % id)

def project_list(request):
    """
    Список всех проектов
    """
    return render_to_response('project_list.html')

def project_add(request):
    """
    Добавление нового проекта
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projects/')
    else:
        form = ProjectForm()
    return render_to_response('new_project.html',{'form': form},
        context_instance=RequestContext(request))

def project_add_bug(request, project_id):
    """
    Добавление бага в проект
    """
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projects/%s' % project_id)
    else:
        form = BugForm(initial={'severity':models.Bug.SEVERITY_CHOICES[0][0]} )
    return render_to_response('addbug.html',locals(),
                              context_instance=RequestContext(request))

def bug_detail(request, id):
    """
    Детали бага
    """
    try:
        bugs = Bug.objects.get(pk=id)
    except Bug.DoesNotExist:
        raise Http404

    if request.user.is_authenticated():
        if ( bugs.project.customer.user == request.user)
            customer_own = project.customer.user

    severity = bugs.get_severity_display()
    status = bugs.get_status_display()
    if request.method == 'POST':
        form = BugDetail(request.POST, initial={'status':bugs.status, 'status_comment':bugs.status_comment}, instance=bugs)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('bugs/show/%s' %id)
    else:
        form = BugDetail(initial={'status':bugs.status,'status_comment':bugs.status_comment})
    return render_to_response('bug_detail.html',locals(),
                context_instance=RequestContext(request))

def bug_list(request):
    """
    Список всех багов
    """
    return render_to_response('bug_list.html')