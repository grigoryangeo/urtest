# File encoding: utf-8
"""
В данном файле содержаться тесты  для видов приложения accounts
"""

from django.test import TestCase
from django.test import Client
from django.core import mail

from enumerations.models import *
from accounts.models import *
from accounts.forms import *
from accounts.views import *


class ViewsTester(TestCase):
    """ Класс для тестрования видов связанных с тестером  """
    fixtures = ['users.json','ProjectBug.json']
    
    def test_registrations(self):
        """  Проверка страницы регистрации """
        
        self.post={
            'email': 'test@test.ru',
            'password': '1233456',
            'password_confirm': '1233456',
            'surname': 'Иванов',
            'name': 'Иван',
            'second_name': 'Иванович',
            'description': 'Нет описания',
            'testing_types': ['4'],
            'os': ['1', '2'],
            'program_languages': ['6'],
            'browsers': ['3', '4'],
         }
        c = Client()
        
        response = c.get('/accounts/testers/register')
        self.assertContains(response, 'Регистрация тестировщика')
        self.assertEqual(response.status_code, 200)

       #self.assertEqual(len(mail.outbox), 1)
       #self.assertEqual(mail.outbox[0].subject, 'Test message')
       #self.assertEqual(mail.outbox[0].body, 'This is a test email')
       #self.assertEqual(mail.outbox[0].from_email, 'from@example.com')
       #self.assertEqual(mail.outbox[0].to[0], self.get1['email'])
       
        response = c.post('/accounts/testers/register', self.post )
        self.assertRedirects(response,'/accounts/thanks')


    def test_tester_detail(self):
        """
        Проверка личной страницы тестировщика
        """
        
        c = Client()
        response = c.get('/accounts/testers/10')
        self.assertEqual(response.status_code, 404)

        response = c.get('/accounts/testers/2')
        self.assertContains(response, 'Личный кабинет тестировщика')
        self.assertEqual(response.status_code, 200)


    def test_tester_edit(self):
        """
        Проверка страницы изменения данных тестировщика
        """
        c = Client()
        response = c.get('/accounts/testers/2/edit')
        self.assertRedirects(response,'/login?next=/accounts/testers/2/edit')

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/accounts/testers/2/edit')
        self.assertEqual(response.status_code, 403)

        c.login(username='Tester@gmail.com', password='123456')
        response = c.get('/accounts/testers/2/edit')
        self.assertContains(response, 'Редактирование личных данных')
        self.assertEqual(response.status_code, 200)

    def test_tester_detail_project(self):
        """
        Проверка страницы  проектов тестировщика
        """
        c = Client()

        response = c.get('/accounts/testers/2/projects')
        self.assertRedirects(response,'/login?next=/accounts/testers/2/projects')

        c.login(username='Tester@gmail.com', password='123456')
        response = c.get('/accounts/testers/2/projects')
        self.assertContains(response, 'Мои проекты')
        self.assertEqual(response.status_code, 200)

        response = c.get('/accounts/testers/10/projects')
        self.assertEqual(response.status_code, 404)


class ViewsCustomer(TestCase):
    """ Класс для тестрования видов связанных с заказчиком  """
    fixtures = ['users.json','ProjectBug.json']

    def test_registrations(self):
        """
        Проверка страницы регистрации  заказчика
        """
         
        c = Client()
        response = c.get('/accounts/customers/register/p')
        self.assertContains(response, 'Регистрация компании')
        self.assertEqual(response.status_code, 200)

        response = c.get('/accounts/customers/register/j')
        self.assertContains(response, 'Регистрация компании')
        self.assertEqual(response.status_code, 200)

        response = c.get('/accounts/customers/register/')
        self.assertContains(response, 'Регистрация компании')
        self.assertEqual(response.status_code, 200)

        response = c.get('/accounts/customers/register/h')
        self.assertEqual(response.status_code, 404)

    def test_customer_detail(self):
        """
        Проверка личной страницы заказчика
        """
        c = Client()
        response = c.get('/accounts/customers/10')
        self.assertRedirects(response,'login?next=/accounts/customers/10')
        self.assertEqual(response.status_code, 302)

        c.login(username='Tester@gmail.com', password='123456')
        response = c.get('/accounts/customers/3')
        self.assertEqual(response.status_code, 403)
        
        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/accounts/customers/3')
        self.assertContains(response, 'Личная страница компании')
        self.assertEqual(response.status_code, 200)

        c.login(username='JurCustomer@gmail.com', password='123456')
        response = c.get('/accounts/customers/4')
        self.assertContains(response, 'Личная страница компании')
        self.assertEqual(response.status_code, 200)


    def test_customer_detail_project(self):
        """
        Проверка страницы  проектов тестировщика
        """
        c = Client()

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/accounts/customers/3/projects')
        self.assertContains(response, 'Мои проекты')
        self.assertEqual(response.status_code, 200)

        c.login(username='JurCustomer@gmail.com', password='123456')
        response = c.get('/accounts/customers/4/projects')
        self.assertContains(response, 'Мои проекты')
        self.assertEqual(response.status_code, 200)

        response = c.get('/accounts/customers/10/projects')
        self.assertEqual(response.status_code, 404)

        c.login(username='Tester@gmail.com', password='123456')
        response = c.get('/accounts/customers/3/projects')
        self.assertEqual(response.status_code, 403)
        
class ViewsRedirectSelf(TestCase):
    """ Класс для тестрования переадресации в свой личный кабинет"""
    fixtures = ['users.json','ProjectBug.json']

    def test_self(self):
        c = Client()

        response = c.get('/accounts/me')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/accounts/me')

        c.login(username='Tester@gmail.com', password='123456')
        response = c.get('/accounts/me')
        self.assertRedirects(response, '/accounts/testers/2')
        self.assertEqual(response.status_code, 302)
       
        c.login(username='JurCustomer@gmail.com', password='123456')
        response = c.get('/accounts/me')
        self.assertRedirects(response, '/accounts/customers/4')
        self.assertEqual(response.status_code, 302)
     
        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.get('/accounts/me')
        self.assertRedirects(response, '/accounts/customers/3')
      
        c.login(username='admin', password='admin')
        response = c.get('/accounts/me')
        #self.assertEqual(response.status_code, 302)
       # self.assertRedirects(response,  '/admin')
       
        c.login(username='BadUser', password='123456')
        response = c.get('/accounts/me')
        self.assertEqual(response.status_code, 404)
