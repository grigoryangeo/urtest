# File encoding: utf-8
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client

from enumerations.models import *
from accounts.models import *
from bugtracker.forms import *
from bugtracker.models import *
from bugtracker.views import *

class ViewsProject(TestCase):
    """ Класс для тестрования отображений связанных с проектом  """
    fixtures = ['users.json','ProjectBug.json']

    def test_project_add(self):
        """ Страница добавления проекта """

        c = Client()
        response = c.post('/bugtracker/projects/add')
        self.assertEqual(response.status_code, 302)

        c.login(username='Tester@gmail.com', password='123456')
        response = c.post('/bugtracker/projects/add')
        self.assertEqual(response.status_code, 403)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/bugtracker/projects/add')
        self.assertEqual(response.status_code, 200)

        response = c.get('/bugtracker/projects/add')
        self.assertEqual(response.status_code, 200)
        
    def test_project_detail(self):
        """ Проверка страницы  деталеи проекта, вкладка с информацией """

        c = Client()
        response = c.post('/bugtracker/projects/10')
        self.assertEqual(response.status_code, 404)
        
        response = c.post('/bugtracker/projects/1')
        self.assertEqual(response.status_code, 200)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/bugtracker/projects/1')
        self.assertEqual(response.status_code, 200)
        
        response = c.post('/bugtracker/projects/1')
        self.assertEqual(response.status_code, 200)

    def test_project_detail_testers(self):
        """ Проверка страницы детали проекта, список тестеров """

        c = Client()
        response = c.post('/bugtracker/projects/10/testers')
        self.assertEqual(response.status_code, 404)

        response = c.post('/bugtracker/projects/1/testers')
        self.assertEqual(response.status_code, 200)

    def test_project_detail_bugs(self):
        """ Проверка страницы детали проекта, список багов """

        c = Client()
        response = c.post('/bugtracker/projects/10/bugs')
        self.assertEqual(response.status_code, 404)
        
        response = c.post('/bugtracker/projects/1/bugs')
        self.assertEqual(response.status_code, 200)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/bugtracker/projects/1/testers')
        self.assertEqual(response.status_code, 200)

    def test_project_add_tester(self):
        """ Проверка страницы добавления тестера """

        c = Client()

        c.logout()
        response = c.post('/bugtracker/projects/1/enlist')
        self.assertEqual(response.status_code, 302)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/bugtracker/projects/10/enlist')
        self.assertEqual(response.status_code, 404)

        response = c.post('/bugtracker/projects/1/enlist')
        self.assertEqual(response.status_code, 403)

        c.login(username='Tester@gmail.com', password='123456')
        response = c.post('/bugtracker/projects/1/enlist')
        # нужно зарегить еще одного тестера
        #self.assertEqual(response.status_code, 200)
      

    def test_project_add_bug(self):
        """ Проверка страницы добавления бага """

        c = Client()

        response = c.post('/bugtracker/projects/10/add_bug')
        self.assertEqual(response.status_code, 302)
        
        response = c.post('/bugtracker/projects/1/add_bug')
        self.assertEqual(response.status_code, 302)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/bugtracker/projects/10/add_bug')
        self.assertEqual(response.status_code, 404)

        response = c.post('/bugtracker/projects/1/add_bug')
        self.assertEqual(response.status_code, 200)

        response = c.get('/bugtracker/projects/1/add_bug')
        self.assertEqual(response.status_code, 200)

    def test_bug_detail(self):
        """ Проверка страницы бага """
        c = Client()

        response = c.post('/bugtracker/bugs/1')
        self.assertEqual(response.status_code, 302)

        
        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/bugtracker/bugs/11')
        self.assertEqual(response.status_code, 404)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/bugtracker/bugs/1')
        self.assertEqual(response.status_code, 200)

        c.login(username='JurCustomer@gmail.com', password='123456')
        response = c.post('/bugtracker/bugs/1')
        self.assertEqual(response.status_code, 200)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/bugtracker/bugs/1')
        self.assertEqual(response.status_code, 200)
