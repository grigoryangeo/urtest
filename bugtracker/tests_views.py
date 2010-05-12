# File encoding: utf-8
"""
В данном файле содержаться тесты  для видов приложения bugtracker
"""

from django.test import TestCase
from django.test import Client

class ViewsProject(TestCase):
    """ Класс для тестрования видов связанных с проектом  """
    fixtures = ['users.json','ProjectBug.json']
    def setUp(self):
        self.post = {
            'program_languages': ['6', '7', '8'],
            'description': 'description',
            'doc_languages': ['1', '2'],
            'size': '10000',
            'name': 'Project2',
        }
             
        self.post_bug = {
            'short_description': 'Name',
            'full_description': 'full_description',
            'finding_description': 'finding_description',
            'severity': '1',
            'test_plan_point':  '0.1.1'
            }

        self.post_Bug_edit={
            'status': 'corrected',
            'status_comment': 'comment'
        }

        
    def test_project_add(self):
        """ Страница добавления проекта """

        c = Client()
        response = c.get('/bugtracker/projects/add')
        self.assertEqual(response.status_code, 302)

        c.login(username='Tester@gmail.com', password='123456')
        response = c.get('/bugtracker/projects/add')
        self.assertEqual(response.status_code, 403)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/bugtracker/projects/add')
        self.assertContains(response, 'Добавление проекта')
        self.assertEqual(response.status_code, 200)

        response = c.post('/bugtracker/projects/add', self.post )
        self.assertRedirects(response,'/bugtracker/projects/2')
        
    def test_project_detail(self):
        """ Проверка страницы  деталеи проекта, вкладка с информацией """

        c = Client()
        response = c.get('/bugtracker/projects/10')
        self.assertEqual(response.status_code, 404)
        
        response = c.get('/bugtracker/projects/1')
        self.assertEqual(response.status_code, 200)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/bugtracker/projects/1')
        self.assertContains(response, 'Детали')
        self.assertEqual(response.status_code, 200)
        

    def test_project_detail_testers(self):
        """ Проверка страницы детали проекта, список тестеров """

        c = Client()
        response = c.get('/bugtracker/projects/10/testers')
        self.assertEqual(response.status_code, 404)

        response = c.get('/bugtracker/projects/1/testers')
        self.assertContains(response, 'Тестировщики')
        self.assertEqual(response.status_code, 200)

    def test_project_detail_bugs(self):
        """ Проверка страницы детали проекта, список багов """

        c = Client()
        response = c.get('/bugtracker/projects/10/bugs')
        self.assertEqual(response.status_code, 404)
        
        response = c.get('/bugtracker/projects/1/bugs')
        self.assertContains(response, 'Баги')
        self.assertEqual(response.status_code, 200)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/bugtracker/projects/1/testers')
        self.assertContains(response, 'Баги')
        self.assertEqual(response.status_code, 200)

    def test_project_add_tester(self):
        """ Проверка страницы добавления тестера к проекту """

        c = Client()

        c.logout()
        response = c.get('/bugtracker/projects/1/enlist')
        self.assertEqual(response.status_code, 302)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/bugtracker/projects/10/enlist')
        self.assertEqual(response.status_code, 404)

        response = c.get('/bugtracker/projects/1/enlist')
        self.assertEqual(response.status_code, 403)

        c.login(username='Tester@gmail.com', password='123456')
        response = c.get('/bugtracker/projects/1/enlist')
        # нужно зарегить еще одного тестера
        #self.assertEqual(response.status_code, 200)
      

    def test_project_add_bug(self):
        """ Проверка страницы добавления бага """
        c = Client()

        response = c.get('/bugtracker/projects/10/add_bug')
        self.assertEqual(response.status_code, 302)
        
        response = c.get('/bugtracker/projects/1/add_bug')
        self.assertEqual(response.status_code, 302)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/bugtracker/projects/10/add_bug')
        self.assertEqual(response.status_code, 404)

        response = c.get('/bugtracker/projects/1/add_bug')
        self.assertContains(response, 'Добавить')
        self.assertEqual(response.status_code, 200)

        response = c.get('/bugtracker/projects/1/add_bug')
        self.assertContains(response, 'Добавить')
        self.assertEqual(response.status_code, 200)

        c.login(username='Tester@gmail.com', password='123456')
        response = c.post('/bugtracker/projects/1/add_bug', self.post_bug)
        self.assertRedirects(response,'/bugtracker/bugs/2')
      

    def test_bug_detail(self):
        """ Проверка страницы бага """

        c = Client()
        response = c.get('/bugtracker/bugs/1')
        self.assertEqual(response.status_code, 302)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/bugtracker/bugs/11')
        self.assertEqual(response.status_code, 404)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/bugtracker/bugs/1')
        self.assertContains(response, 'Страница')
        self.assertEqual(response.status_code, 200)

        c.login(username='JurCustomer@gmail.com', password='123456')
        response = c.get('/bugtracker/bugs/1')
        self.assertContains(response, 'Страница')
        self.assertEqual(response.status_code, 200)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/bugtracker/bugs/1')
        self.assertContains(response, 'Страница')
        self.assertEqual(response.status_code, 200)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/bugtracker/bugs/1', self.post_Bug_edit)
        self.assertRedirects(response,'/accounts/customers/3')

