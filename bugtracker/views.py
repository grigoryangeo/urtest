# File encoding: utf-8

def project_detail(request, id):
    """
    Детали проекта, вкладка с информацией
    """
    pass

def project_detail_testers(request, id):
    """
    Детали проекта, вкладка со списком тестеров
    """
    pass

def project_detail_bugs(request, id):
    """
    Детали проекта, вкладка со списком багов
    """
    pass

def project_add_tester(request, id):
    """
    Добавление авторизованного тестера к проекту
    """
    pass

def project_list(request):
    """
    Список всех проектов
    """
    pass

def project_add(request):
    """
    Добавление нового проекта
    """
    pass

def project_add_bug(request, project_id):
    """
    Добавление бага в проект
    """
    pass

def bug_detail(request, id):
    """
    Детали бага
    """
    pass

def bug_list(request):
    """
    Список всех багов
    """