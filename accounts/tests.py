# File encoding: utf-8
"""
В данном файле содержаться тесты форм для приложения accounts
"""

from django.test import TestCase

from accounts.models import *
from accounts.forms import *

class Valdation(TestCase):
    """ Наследуемый класс содержащий метод для валидации форм """

    def check_valid(self, post, form_type, ch, inst ):
        if inst :
            form = form_type(post, instance=inst)
        else:
            form = form_type(post)
        if ch:
            assert form.is_valid()
            form.save()
        else:
            assert not form.is_valid()


class TesterRegister( Valdation):
    """ Класс для тестирования формы регистрации тестировщика """
    fixtures = ['users.json']

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

        self.post_password_conf={
            'email': 'test@test.ru',
            'password': '1233456',
            'password_confirm': '1233457',
            'surname': 'Иванов',
            'name': 'Иван',
            'second_name': 'Иванович',
            'description': 'Нет описания',
            'testing_types': ['4'],
            'os': ['1', '2'],
            'program_languages': ['6'],
            'browsers': ['3', '4'],
         }
        self.post_exist={
            'email': 'tester@gmail.ru',
            'password': '1233456',
            'password_confirm': '1233457',
            'surname': 'Иванов',
            'name': 'Иван',
            'second_name': 'Иванович',
            'description': 'Нет описания',
            'testing_types': ['4'],
            'os': ['1', '2'],
            'program_languages': ['6'],
            'browsers': ['3', '4'],
         }

    def test_register(self):
        """
        Проверка формы регистрации тестировщика на валидность.
        ( случай хороших данных)
        """
        self.check_valid(self.post, TesterRegForm, True, None)

        try:
            self.tester=Tester.objects.get(email= self.post['email'])
        except Tester.DoesNotExist:
            print  "Object Not found"
            assert(False)

        self.assertEquals(self.tester.surname, u'Иванов')
        self.assertEquals(self.tester.name, u'Иван')
        self.assertEquals(self.tester.second_name, u'Иванович')
        self.assertEquals(self.tester.description, u'Нет описания')
        assert self.tester.check_password(self.post['password'])

        self.assertEquals([str(os.pk) for os in self.tester.os.all().order_by('pk')],
                          self.post['os'])
        self.assertEquals([str(browser.pk) for browser in self.tester.browsers.all().order_by('pk')],
                          self.post['browsers'])
        self.assertEquals([str(program_language.pk) for program_language in
                          self.tester.program_languages.all().order_by('pk')],
                          self.post['program_languages'])
        self.assertEquals([str(testing_types.pk) for testing_types in self.tester.testing_types.all().order_by('pk')],
                          self.post['testing_types'])

    def test_register_exist(self):
        """
         Пытаемся зарегистрировать уже существующего тестировщика
        """

        self.check_valid(self.post_exist, TesterRegForm, False, None)



    def test_register_password(self):
        """
         Пароль и подтверждение в форме не совпадают
        """

        self.check_valid(self.post_password_conf, TesterRegForm, False, None )


class TesterEdit(Valdation):
     """ Класс для тестирования формы изменения данных тестировщика """
     fixtures = ['users.json']

     def setUp(self):
        self.post={
            'password': '654321',
            'password_confirm': '654321',
            'description': 'Not',
            'testing_types': ['4'],
            'os': ['4'],
            'program_languages': ['7'],
            'browsers': ['5'],
         }

        self.post_password_conf={
            'password': '654321',
            'password_confirm': '654329',
            'description': 'Нет описания',
            'testing_types': ['4'],
            'os': ['1', '2'],
            'program_languages': ['6'],
            'browsers': ['3', '4'],
         }

     def test_edit(self):
        """
        Проверка формы изменения данных тестера
        ( случай хороших данных )
        """
        try:
            self.tester=Tester.objects.get(email='tester@gmail.com')
        except Tester.DoesNotExist:
            print  "Object Not found"
            assert(False)

        self.check_valid(self.post, TesterChangeForm, True, self.tester )

        self.assertEquals(self.tester.description, self.post['description'])
        assert self.tester.check_password(self.post['password'])

        self.assertEquals([str(os.pk) for os in self.tester.os.all().order_by('pk')],
                          self.post['os'])
        self.assertEquals([str(browser.pk) for browser in self.tester.browsers.all().order_by('pk')],
                          self.post['browsers'])
        self.assertEquals([str(program_language.pk) for program_language in
                          self.tester.program_languages.all().order_by('pk')],
                          self.post['program_languages'])
        self.assertEquals([str(testing_types.pk) for testing_types in
                          self.tester.testing_types.all().order_by('pk')],
                          self.post['testing_types'])
        assert self.tester.check_password(self.post['password'])

     def test_edit_password(self):
        """
        Пароль и подтверждение  не совпадают
        """

        self.check_valid(self.post_password_conf, TesterChangeForm, False, None )

class JurCustomerRegister(Valdation):
    """ Класс для тестирования формы регистрации юридического лица """
    fixtures = ['users.json']
    def setUp(self):
        self.post={
            'type':'j',
            'email': 'jur@test.ru',
            'password': '1233456',
            'password_confirm': '1233456',
            'name': 'Иван',
            'inn':'123456',
            'bank_account':'123456',
            'bank':'123445',
            'kpp':'234545',
            'bik':'1222222',
            'correspondent_account':'111111',
            'ogrn':'1111111111',
            'phone':'666-66-66',
            'www':'www.google.ru',
            'address_ur':'www.google.ru',
            'description':'No',
            'repr_surname':'Иванов',
            'repr_name':'Иван',
            'repr_second_name':'Иванович',
            'repr_phone':'666-66-66',
            'pay_type':['1'],
         }

        self.post_exist={
            'type':'j',
            'email': ' JurCustomer@gmail.com',
            'password': '1233456',
            'password_confirm': '1233456',
            'name': 'Иван',
            'inn':'123456',
            'bank_account':'123456',
            'bank':'123445',
            'kpp':'234545',
            'bik':'1222222',
            'correspondent_account':'111111',
            'ogrn':'1111111111',
            'phone':'666-66-66',
            'www':'www.google.ru',
            'address_ur':'www.google.ru',
            'description':'No',
            'repr_surname':'Иванов',
            'repr_name':'Иван',
            'repr_second_name':'Иванович',
            'repr_phone':'666-66-66',
            'pay_type':['1'],
         }

        self.post_password={
            'type':'j',
            'email': ' JurCustomer@gmail.com',
            'password': '1233456',
            'password_confirm': '1233457',
            'name': 'Иван',
            'inn':'123456',
            'bank_account':'123456',
            'bank':'123445',
            'kpp':'234545',
            'bik':'1222222',
            'correspondent_account':'111111',
            'ogrn':'1111111111',
            'phone':'666-66-66',
            'www':'www.google.ru',
            'address_ur':'www.google.ru',
            'description':'No',
            'repr_surname':'Иванов',
            'repr_name':'Иван',
            'repr_second_name':'Иванович',
            'repr_phone':'666-66-66',
            'pay_type':['1'],
         }

    def valid(self,post,bool):
        self.form = JurCustomerRegForm(post)
        if bool==1:
            assert self.form.is_valid()
            self.form.save()
            try:
                self.customer=JurCustomer.objects.get(email=post['email'])
            except JurCustomer.DoesNotExist:
                print  "Object Not found"
                assert(False)
        else:
            assert not self.form.is_valid()

    def test_register(self):
        """
        Проверка формы регистрации юридического лица .
        Случай хороших данных.
        """
        self.check_valid(self.post, JurCustomerRegForm, True, None )

        try:
            self.customer=JurCustomer.objects.get(email= self.post['email'])
        except JurCustomer.DoesNotExist:
            print  "Object Not found"
            assert(False)

        self.assertEquals(self.customer.repr_surname, u'Иванов')
        self.assertEquals(self.customer.repr_name, u'Иван')
        self.assertEquals(self.customer.repr_second_name, u'Иванович')
        self.assertEquals(self.customer.description, self.post['description'])
        self.assertEquals( str(self.customer.inn), self.post['inn'])
        self.assertEquals( str(self.customer.bank_account), self.post['bank_account'])
        self.assertEquals( str(self.customer.bank), self.post['bank'])
        self.assertEquals( str(self.customer.kpp), self.post['kpp'])
        self.assertEquals( str(self.customer.bik), self.post['bik'])
        self.assertEquals(self.customer.correspondent_account, self.post['correspondent_account'])
        self.assertEquals(self.customer.ogrn, self.post['ogrn'])
        self.assertEquals(self.customer.phone, self.post['phone'])
        self.assertEquals(self.customer.repr_phone, self.post['repr_phone'])
        self.assertEquals(self.customer.address_ur, self.post['address_ur'])

        assert self.customer.check_password(self.post['password'])

        self.assertEquals([str(pay_type.pk) for pay_type in self.customer.pay_type.all().order_by('pk')],
                          self.post['pay_type'])

    def test_customer_exist(self):
        """
         Пытаемся зарегистрировать уже существующее  юридическое лицо
        """
        self.check_valid(self.post_exist, JurCustomerRegForm, False, None )

    def test_customer_password(self):
        """
         Пароль и подтверждение не совпадают
        """

        self.check_valid(self.post_password, JurCustomerRegForm, False, None )


class PhisCustomerRegister(Valdation):
    """ Класс для тестирования формы регистрации физического лица """
    fixtures = ['users.json']

    def setUp(self):
         self.post={
            'type':'p',
            'email': 'phis@test.ru',
            'password': '1233456',
            'password_confirm': '1233456',
            'phone':'666-66-66',
            'passport_who':'www.google.ru',
            'passport_number':'666666',
            'description':'No',
            'passport_when_day':'12',
            'passport_when_month':'12',
            'passport_when_year':'2000',
            'surname':'Иванов',
            'name':'Иван',
            'second_name':'Иванович',
            'passport_series':'6666666',
            'pay_type':['1']
         }
         self.post_exist={
            'type':'p',
            'email': 'PhisCustomer@gmail.com',
            'password': '1233456',
            'password_confirm': '1233456',
            'phone':'666-66-66',
            'passport_who':'www.google.ru',
            'passport_number':'666666',
            'description':'No',
            'passport_when_day':'12',
            'passport_when_month':'12',
            'passport_when_year':'2000',
            'surname':'Иванов',
            'name':'Иван',
            'second_name':'Иванович',
            'passport_series':'6666666',
            'pay_type':['1']
         }

         self.post_password={
            'type':'p',
            'email': 'phis@test.ru',
            'password': '1233456',
            'password_confirm': '2233456',
            'phone':'666-66-66',
            'passport_who':'www.google.ru',
            'passport_number':'666666',
            'description':'No',
            'passport_when_day':'12',
            'passport_when_month':'12',
            'passport_when_year':'2000',
            'surname':'Иванов',
            'name':'Иван',
            'second_name':'Иванович',
            'passport_series':'6666666',
            'pay_type':['1']
         }

    def test_register(self):
        """
        Проверка формы регистрации физического лица
        (Случай хороших данных)
        """

        self.check_valid(self.post, PhysCustomerRegForm, True, None )

        try:
            self.customer=PhysCustomer.objects.get(email= self.post['email'])
        except PhysCustomer.DoesNotExist:
            print  "Object Not found"
            assert(False)

        self.assertEquals(self.customer.surname, u'Иванов')
        self.assertEquals(self.customer.name, u'Иван')
        self.assertEquals(self.customer.second_name, u'Иванович')
        self.assertEquals(self.customer.phone, self.post['phone'])

        self.assertEquals([str(pay_type.pk) for pay_type in self.customer.pay_type.all().order_by('pk')],
                          self.post['pay_type'])

        assert self.customer.check_password(self.post['password'])

    def test_customer_exist(self):
        """ Заказчик уже существует . """

        self.check_valid(self.post_exist, PhysCustomerRegForm, False, None )

    def test_customer_password(self):
        """ Пароль и подтверждение гнен совпадают  """

        self.check_valid(self.post_password, PhysCustomerRegForm, False, None )


