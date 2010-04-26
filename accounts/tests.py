# File encoding: utf-8
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from enumerations.models import *
from accounts.models import *

from accounts.forms import *


from accounts.models import Tester

from django.test import TestCase
from django.shortcuts import get_object_or_404


class TesterRegister(TestCase):
    fixtures = ['user.json']
    
    def setUp(self):
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
    
    def test_tester_register(self):
        """
        Проверка формы регистрации тестировщика ( TesterRegForm)
        на валидность.
        
        """
       

        form = TesterRegForm(self.post) 
        assert form.is_valid()
        form.save()

        try:
            tester=Tester.objects.get(email='test@test.ru')
        except Tester.DoesNotExist:
            print  "Object Not found"
            assert(False)

    
        self.assertEquals(tester.surname, u'Иванов')
        self.assertEquals(tester.name, u'Иван')
        self.assertEquals(tester.second_name, u'Иванович')
        self.assertEquals(tester.description, u'Нет описания')
        self.assertEquals(tester.testing_types.all()[0].name, u'Функциональное')
        assert tester.check_password(self.post['password'])

        self.assertEquals([str(os.pk) for os in tester.os.all().order_by('pk')],
                          self.post['os'])
        self.assertEquals([str(browser.pk) for browser in tester.browsers.all().order_by('pk')],
                          self.post['browsers'])
        self.assertEquals([str(program_language.pk) for program_language in
                           tester.program_languages.all().order_by('pk')],
                          self.post['program_languages'])
  

class CustomerRegister(TestCase):
    def setUp(self):
        browser=Browser.objects.get(pk=1)
        os=OS.objects.get(pk=1)
        progLang=ProgramLanguage.objects.get(pk=1)
        testtype=TestingType.objects.get(pk=1)
        paytype=PayType.objects.get(pk=1)
        lang=Language.objects.get(pk=1)
        pass

    def test_jur_customer_register(self):
        """
        Tests that 1 + 1 always equals 2.
        """

        post={
        'email': 'gamer143@yandex.ru',
        'password': '1233456',
        'password_confirm': '1233456',
        'surname': 'Иванов',
        'name': 'Иван',
        'second_name': 'Иванович',
        'description': 'Нет описания',
        'testing_types': ['4'],
        'os': ['1', '2', '3'],
        'program_languages': ['6', '7', '2'],
        'browsers': ['3', '4'],
        'submit': 'Submit'
         }

        form = JurCustomerRegForm(post)
        #assert(form.is_valid())
        #form.save()
        
    def test_phys_customer_register(self):
        """
        Tests that 1 + 1 always equals 2.
        """

        post={
        'email': 'gamer143@yandex.ru',
        'password': '1233456',
        'password_confirm': '1233456',
        'surname': 'Иванов',
        'name': 'Иван',
        'second_name': 'Иванович',
        'description': 'Нет описания',
        'testing_types': ['4'],
        'os': ['1', '2', '3'],
        'program_languages': ['6', '7', '2'],
        'browsers': ['3', '4'],
        'submit': 'Submit'
         }

        form = PhysCustomerRegForm(post)
        #assert(form.is_valid())
        #form.save()
      
