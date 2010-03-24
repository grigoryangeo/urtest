# File encoding: utf-8

def tester_detail(request, id):
    """Детали тестера
    
    Параметры:
        id - ключ
    """
    pass

def tester_detail_projects(request, id):
    """
    Детали тестера, вкладка со списком проектов тестера
    """
    pass

def tester_list(request):
    """Список тестеров"""
    pass

def tester_registration(request):
    """Регистрация тестера"""
    pass

def company_detail(request, id):
    """Детали компании
    
    Параметры:
        id - ключ
    """
    pass

def company_detail_projects(request, id):
    """
    Детали компании, вкладка со списком проектов компании
    """
    pass

def company_registration(request, type):
    """Детали компании
    
    Параметры:
        type - j либо p, Физ/Юр лицо
    """
    pass

def company_list(request):
    """Список компаний"""
    pass

def redirect_to_self(request):
    """Переадресация в свой личный кабинет"""
    pass
