# File encoding: utf-8
"""
В данном файле содержаться тесты отоюражений для приложения accounts
"""

from django.test import TestCase
from django.test import Client
from django.core import mail

from enumerations.models import *
from accounts.models import *
from accounts.forms import *
from accounts.views import *


class ViewsTester(TestCase):
    """ Класс для тестрования отображений связанных с тестером  """
    fixtures = ['users.json','ProjectBug.json']
    
    def test_registrations(self):
        """  Проверка страницы регистрации """

        c = Client()
        response = c.post('/accounts/testers/register')
        self.assertEqual(response.status_code, 200)

       #self.assertEqual(len(mail.outbox), 1)
       #self.assertEqual(mail.outbox[0].subject, 'Test message')
       #self.assertEqual(mail.outbox[0].body, 'This is a test email')
       #self.assertEqual(mail.outbox[0].from_email, 'from@example.com')
       #self.assertEqual(mail.outbox[0].to[0], self.post1['email'])

        response = c.get('/accounts/testers/register')
        self.assertEqual(response.status_code, 200)


    def test_tester_detail(self):
        """
        Проверка личной страницы тестировщика
        """
        
        c = Client()
        response = c.post('/accounts/testers/10')
        self.assertEqual(response.status_code, 404)

        response = c.post('/accounts/testers/2')
        self.assertEqual(response.status_code, 200)


    def test_tester_edit(self):
        """
        Проверка страницы изменения данных тестировщика
        """
        c = Client()
        response = c.post('/accounts/testers/2/edit')
        self.assertEqual(response.status_code, 302)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/accounts/testers/2/edit')
        self.assertEqual(response.status_code, 403)

        c.login(username='Tester@gmail.com', password='123456')
        response = c.post('/accounts/testers/2/edit')
        self.assertEqual(response.status_code, 200)

    def test_tester_detail_project(self):
        """
        Проверка страницы  проектов тестировщика
        """
        c = Client()

        c.login(username='Tester@gmail.com', password='123456')
        response = c.post('/accounts/testers/2/projects')
        self.assertEqual(response.status_code, 200)

        response = c.post('/accounts/testers/10/projects')
        self.assertEqual(response.status_code, 404)


class ViewsCustomer(TestCase):
    """ Класс для тестрования отображений связанных с заказчиком  """
    fixtures = ['users.json','ProjectBug.json']

    def test_registrations(self):
        """
        Проверка страницы регистрации  заказчика
        """
        
        c = Client()
        response = c.post('/accounts/customers/register/p')
        self.assertEqual(response.status_code, 200)

        response = c.post('/accounts/customers/register/j')
        self.assertEqual(response.status_code, 200)

        response = c.post('/accounts/customers/register/')
        self.assertEqual(response.status_code, 200)

        response = c.post('/accounts/customers/register/h')
        self.assertEqual(response.status_code, 404)


    def test_customer_detail(self):
        """
        Проверка личной страницы тестировщика
        """
        c = Client()
        response = c.post('/accounts/customers/10')
        self.assertEqual(response.status_code, 302)

        c.login(username='Tester@gmail.com', password='123456')
        response = c.post('/accounts/customers/3')
        self.assertEqual(response.status_code, 403)

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/accounts/customers/3')
        self.assertEqual(response.status_code, 200)

        c.login(username='JurCustomer@gmail.com', password='123456')
        response = c.post('/accounts/customers/4')
        self.assertEqual(response.status_code, 200)


    def test_customer_detail_project(self):
        """
        Проверка страницы  проектов тестировщика
        """
        c = Client()

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/accounts/customers/3/projects')
        self.assertEqual(response.status_code, 200)

        c.login(username='JurCustomer@gmail.com', password='123456')
        response = c.post('/accounts/customers/4/projects')
        self.assertEqual(response.status_code, 200)

        response = c.post('/accounts/customers/10/projects')
        self.assertEqual(response.status_code, 404)

        c.login(username='Tester@gmail.com', password='123456')
        response = c.post('/accounts/customers/3/projects')
        self.assertEqual(response.status_code, 403)
        
class ViewsRedirectSelf(TestCase):
    """ Класс для тестрования переадресация в свой личный кабинет"""
    fixtures = ['users.json','ProjectBug.json']

    def test_self(self):
        c = Client()

        response = c.post('/accounts/me')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/accounts/me')

        c.login(username='Tester@gmail.com', password='123456')
        response = c.post('/accounts/me')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/testers/2')

        c.login(username='JurCustomer@gmail.com', password='123456')
        response = c.post('/accounts/me')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/customers/4')

        c.login(username='PhisCustomer@gmail.com', password='123456')
        response = c.post('/accounts/me')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/customers/3')

        #c.login(username='admin', password='admin')
        #response = c.post('/accounts/me')
       # self.assertEqual(response.status_code, 302)
       # self.assertRedirects(response, '/admin')
