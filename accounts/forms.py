# File encoding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import CheckboxSelectMultiple

from lib.fields import UrtestTextAreaField, UrtestPasswordField, UrtestFIOField
from enumerations import models as enum
from accounts import models


class UserForm(forms.ModelForm):
    email = forms.EmailField(label='Контактный E-mail', max_length=50)
    password = UrtestPasswordField(label='Пароль')
    password_confirm = UrtestPasswordField(label='Подтверждение пароля')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Такой адрес уже зарегистрирован')

    def clean_password_confirm(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return password_confirm

    def save(self, *args, **kwargs):
        assert(self.is_valid())
        # Вызов оригинального save
        data = self.cleaned_data
        user = super(forms.ModelForm, self).save(commit=False, *args, **kwargs)
        user.username = user.email = data['email']
        user.set_password(data['password'])
        user.save()
        self.save_m2m()
        return user


class JurCustomerRegForm(UserForm):
    #type = forms.CharField(widget=forms.HiddenInput, initial='j')
    address_ur = UrtestTextAreaField(label="Юридический адрес компании")
    description = UrtestTextAreaField(label="Информация о компании")
    repr_surname = UrtestFIOField(label="Фамилия заказчика", max_length=80)
    repr_name = UrtestFIOField(label="Имя заказчика", max_length=30)
    repr_second_name = UrtestFIOField(label="Отчество заказчика", max_length=50, required=False)
    pay_type = forms.ModelMultipleChoiceField(label="Способ оплаты",
                                              queryset=enum.PayType.objects.all(),
                                              widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = models.JurCustomer
        fields = ['email', 'password', 'password_confirm'] + [
            'name',
            'inn',
            'bank_account',
            'bank',
            'kpp',
            'bik',
            'correspondent_account',
            'ogrn',
            'phone',
            'www',
            'address_ur',
            'description',
            'repr_surname',
            'repr_name',
            'repr_second_name',
            'repr_phone',
            'pay_type',
        ]


class PhysCustomerRegForm(UserForm):
    #type = forms.CharField(widget=forms.HiddenInput, initial='p')
    surname = UrtestFIOField(label="Фамилия заказчика", max_length=80)
    name = UrtestFIOField(label="Имя заказчика", max_length=30)
    second_name = UrtestFIOField(label="Отчество заказчика", max_length=50, required=False)
    pay_type = forms.ModelMultipleChoiceField(label="Способ оплаты", queryset=enum.PayType.objects.all(), widget=forms.CheckboxSelectMultiple)
    passport_when = forms.DateField(label="Дата выдачи", widget=SelectDateWidget(years=range(2010, 1900, -1)))

    class Meta:
        model = models.PhysCustomer
        exclude = ['customer']
        fields = ['email', 'password', 'password_confirm'] + [
            'surname',
            'name',
            'second_name',
            'passport_series',
            'passport_number',
            'passport_when',
            'passport_who',
            'phone',
            'pay_type',
        ]



class TesterRegForm(UserForm):
    surname = UrtestFIOField(label="Фамилия", max_length=80)
    name = UrtestFIOField(label="Имя", max_length=30)
    second_name = UrtestFIOField(label="Отчество", max_length=30, required=False)
    description = UrtestTextAreaField(label="О себе", required=False)
    os = forms.ModelMultipleChoiceField(label="Операционные системы",
                                        queryset=enum.OS.objects.all(),
                                        widget=CheckboxSelectMultiple)
    program_languages = forms.ModelMultipleChoiceField(label="Языки программирования",
                                                       queryset=enum.ProgramLanguage.objects.all(),
                                                       widget=CheckboxSelectMultiple)
    testing_types = forms.ModelMultipleChoiceField(label="Типы тестирования",
                                                   queryset=enum.TestingType.objects.all(),
                                                   widget=CheckboxSelectMultiple)
    browsers = forms.ModelMultipleChoiceField(label="Браузеры",
                                              queryset=enum.Browser.objects.all(),
                                              widget=CheckboxSelectMultiple)

    class Meta:
        model = models.Tester
        fields = ['email', 'password', 'password_confirm',
                  'surname', 'name', 'second_name',
                  'os', 'program_languages', 'testing_types', 'browsers', 'description']


class TesterChangeForm(forms.ModelForm):
    password = UrtestPasswordField(label='Пароль', required=False)
    password_confirm = UrtestPasswordField(label='Подтверждение пароля',
                                           required=False)
    os = forms.ModelMultipleChoiceField(label="Операционные системы",
                                              queryset=enum.OS.objects.all(),
                                              widget=CheckboxSelectMultiple)
    program_languages = forms.ModelMultipleChoiceField(label="Языки программирования",
                                                       queryset=enum.ProgramLanguage.objects.all())
    testing_types = forms.ModelMultipleChoiceField(label="Типы тестирования",
                                                   queryset=enum.TestingType.objects.all())
    browsers = forms.ModelMultipleChoiceField(label="Браузеры", queryset=enum.Browser.objects.all())
    description = UrtestTextAreaField(label="О себе", required=False)

    class Meta:
        model = models.Tester
        fields = ['password', 'password_confirm', 'os', 'program_languages', 'testing_types', 'browsers', 'description']

    def save(self, *args, **kwargs):
        """Обновление тестера с учетом смены пароля"""
        # Вызов оригинального save
        data = self.cleaned_data
        tester = super(TesterChangeForm, self).save(*args, **kwargs)
        # Проверка на смену пароля
        if data['password']:
            # Пароль изменился
            tester.set_password(data['password'])
            tester.save()
        return tester

    def clean(self):
        # Вызов оригинального clean()
        data = super(TesterChangeForm, self).clean()
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Неправильно введены данные')
        return data



class JurCustomerChangeForm(forms.ModelForm):
    password = UrtestPasswordField(label='Пароль', required=False)
    password_confirm = UrtestPasswordField(label='Подтверждение пароля',
                                           required=False)

    repr_surname = UrtestFIOField(label="Фамилия заказчика", max_length=80)
    repr_name = UrtestFIOField(label="Имя заказчика", max_length=30)
    repr_second_name = UrtestFIOField(label="Отчество заказчика", max_length=50, required=False)
    pay_type = forms.ModelMultipleChoiceField(label="Способ оплаты",
                                              queryset=enum.PayType.objects.all())
    #testing_types = forms.ModelMultipleChoiceField(label="Способ оплаты",
   #                                                queryset=enum.TestingType.objects.all())


    class Meta:
        model = models.JurCustomer
        fields = ['password',
        'password_confirm',
        'name',
        'repr_surname',
        'repr_name',
        'repr_second_name',
        'address_ur',
        'pay_type',
        'inn',
        'bank_account',
        'bank',
        'kpp',
        'bik',
        'correspondent_account',
        'ogrn',
        'phone']

    def save(self, *args, **kwargs):
        """Обновление заказчика с учетом смены пароля"""
        # Вызов оригинального save
        data = self.cleaned_data
        customer = super(JurCustomerChangeForm, self).save(*args, **kwargs)
        # Проверка на смену пароля
        if data['password']:
            # Пароль изменился
            customer.set_password(data['password'])
            customer.save()
        return customer

    def clean(self):
        # Вызов оригинального clean()
        data = super(JurCustomerChangeForm, self).clean()
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return data

class PhysCustomerChangeForm(forms.ModelForm):
    password = UrtestPasswordField(label='Пароль', required=False)
    password_confirm = UrtestPasswordField(label='Подтверждение пароля',
                                           required=False)
    surname = UrtestFIOField(label="Фамилия заказчика", max_length=80)
    name = UrtestFIOField(label="Имя заказчика", max_length=30)
    second_name = UrtestFIOField(label="Отчество заказчика", max_length=50, required=False)
    passport_when = forms.DateField(label="Дата выдачи", widget=SelectDateWidget(years=range(2010, 1900, -1)))
    pay_type = forms.ModelMultipleChoiceField(label="Способ оплаты",
                                            queryset=enum.PayType.objects.all())
    #testing_types = forms.ModelMultipleChoiceField(label="Способ оплаты",
   #                                                queryset=enum.TestingType.objects.all())


    class Meta:
        model = models.PhysCustomer
        fields = ['password', 'password_confirm',
            'surname',
            'name',
            'second_name',
            'passport_series',
            'passport_number',
            'passport_when',
            'passport_who',
            'phone',
            'pay_type',
            'pay_type']
    
    def save(self, *args, **kwargs):
        """Обновление заказчика с учетом смены пароля"""
        # Вызов оригинального save
        data = self.cleaned_data
        customer = super(PhysCustomerChangeForm, self).save(*args, **kwargs)
        # Проверка на смену пароля
        if data['password']:
            # Пароль изменился
            customer.set_password(data['password'])
            customer.save()
        return customer

    def clean(self):
        # Вызов оригинального clean()
        data = super(PhysCustomerChangeForm, self).clean()
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return data
