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
        browser=Browser.objects.get(pk=1)
        os=OS.objects.get(pk=1)
        progLang=ProgramLanguage.objects.get(pk=1)
        testtype=TestingType.objects.get(pk=1)
        paytype=PayType.objects.get(pk=1)
        lang=Language.objects.get(pk=1)
        pass
    
    def test_tester_register(self):
        """
        Проверка формы регистрации тестировщика ( TesterRegForm)
        на валидность.
        
        """
       
        post={
        'email': 'test@test.ru',
        'password': '1233456',
        'password_confirm': '1233456',
        'surname': 'Иванов',
        'name': 'Иван',
        'second_name': 'Иванович',
        'description': 'Нет описания',
        'testing_types': ['4'],
        'os': ['1'],
        'program_languages': ['6'],
        'browsers': ['3'],
        'submit': 'Submit'
         }

        form = TesterRegForm(post) 
        assert(form.is_valid())
        form.save()

        try:
            tester=Tester.objects.get(email='test@test.ru')
        except Tester.DoesNotExist:
            print  "Object Not found"
            assert(False)

    
        assert(tester.surname==u'Иванов')
        assert(tester.name==u'Иван')
        assert(tester.second_name==u'Иванович')
        assert(tester.description==u'Нет описания')
        assert(tester.testing_types.all()[0].name==u'Функциональное')
        assert(tester.os.all()[0].name==u'Linux')
        assert(tester.os.all()[0].name==u'Linux')
        assert(tester.program_languages.all()[0].name==u'C')
        assert(tester.browsers.all()[0].name==u'Mozilla Firefox')
  

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
      
