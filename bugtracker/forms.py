# File encoding: utf-8
from django.core.exceptions import ObjectDoesNotExist
from django import forms
import bugtracker.models as models
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple


class BugForm(forms.ModelForm):
    short_description = forms.CharField(label="Краткое описание")
    severity = forms.CharField(label="Критичность", widget=forms.RadioSelect(choices=models.Bug.SEVERITY_CHOICES))
    #file_comment=forms.CharField(label="Комментариии к файлу" ,widget=forms.Textarea, required=False,max_length=150)
    class Meta:
        model = models.Bug
        exclude = ['tester', 'status', 'status_comment', 'project']

class BugDetail(forms.ModelForm):
    status = forms.CharField(label="Статус", widget=forms.RadioSelect(choices=models.Bug.STATUS_CHOICES))
    status_comment = forms.CharField(label="Примичание", widget=forms.Textarea, required=False)
    class Meta:
        model = models.Bug
        fields=['status','status_comment']

class ProjectForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if models.Project.objects.filter(name=name).count() > 0:
            raise forms.ValidationError('Проект с таким названием уже существует')
        return name
    class Meta:
        model = models.Project
        exclude = ['customer', 'testers']


class UserForm(forms.ModelForm):
    email = forms.EmailField(label='Контактный E-mail')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(render_value=False))
    accept = forms.BooleanField(label='Договор', required=False, help_text='Я согласен с условиями договора')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).count() > 0:
            raise forms.ValidationError('Пользователь с таким адресом уже существует')
        return email

    def clean_accept(self):
        accept = self.cleaned_data.get('accept')
        if accept == 0 :
            raise forms.ValidationError('Необходимо подтверждение согласия с пользовательским договором')
        return accept
   
    def clean_password_confirm(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return password_confirm


class TesterForm(forms.Form):
    email = forms.EmailField(label='E-mail')

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(render_value=False), required=False)
    password_confirm = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(render_value=False), required=False)
    last_name = forms.CharField(label="Фамилия")
    first_name = forms.CharField(label="Имя")
    second_name = forms.CharField(label="Отчество")
    description = forms.CharField(label="О себе", widget=forms.Textarea, required=False)

    os = forms.ModelMultipleChoiceField(label="Операционные системы", queryset=models.OSystem.objects.all(), widget=FilteredSelectMultiple(u'ОС', False))
    #os = forms.ModelMultipleChoiceField(queryset=models.OSystem.objects.all())
    program_languages = forms.ModelMultipleChoiceField(label="Языки программирования", queryset=models.ProgramLang.objects.all(), widget=FilteredSelectMultiple(u'языки', False))
    testing_types = forms.ModelMultipleChoiceField(label="Типы тестирования", queryset=models.TestingType.objects.all(), widget=FilteredSelectMultiple(u'типы', False))
    browsers = forms.ModelMultipleChoiceField(label="Браузеры", queryset=models.Browser.objects.all(), widget=FilteredSelectMultiple(u'браузеры', False))

    accept = forms.BooleanField(label='Договор', required=False, help_text='Я согласен с условиями договора')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).count() > 0:
            raise forms.ValidationError('Пользователь с таким адресом уже существует')
        return email

    def clean_accept(self):
        accept = self.cleaned_data.get('accept')
        if accept == 0 :
            raise forms.ValidationError('Необходимо подтверждение согласия с пользовательским договором')
        return accept

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return cleaned_data


class UrCustomerForm(UserForm):
    type = forms.CharField(widget=forms.HiddenInput, initial='y')
    pay_type = forms.ModelMultipleChoiceField(label="Способ оплаты", queryset=models.PayingType.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = models.UrCustomer
        exclude = ['customer']
        fields = ['type', 'email', 'password', 'password_confirm'] + [f.name for f in models.UrCustomer._meta.fields[2:]] + [f.name for f in models.UrCustomer._meta.many_to_many] + ['accept']


class PhysCustomerForm(UserForm):
    type = forms.CharField(widget=forms.HiddenInput, initial='f')
    pay_type = forms.ModelMultipleChoiceField(label="Способ оплаты", queryset=models.PayingType.objects.all(), widget=forms.CheckboxSelectMultiple)

    
    class Meta:
        model = models.PhysCustomer
        exclude = ['customer']
        fields = ['type', 'email', 'password', 'password_confirm'] + [f.name for f in models.PhysCustomer._meta.fields[2:]] + [f.name for f in models.PhysCustomer._meta.many_to_many] + ['accept']

class TesterDetailForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(render_value=False))
    
    osystems = forms.ModelMultipleChoiceField(label="Операционные системы", queryset=models.OSystem.objects.all())
    program_languages = forms.ModelMultipleChoiceField(label="Языки программирования", queryset=models.ProgramLang.objects.all())
    testing_types = forms.ModelMultipleChoiceField(label="Типы тестирования", queryset=models.TestingType.objects.all())
    browsers = forms.ModelMultipleChoiceField(label="Браузеры", queryset=models.Browser.objects.all())

    description = forms.CharField(label="О себе", widget=forms.Textarea, required=False)

    class Meta:
        model = models.Tester
        fields = ['password', 'password_confirm', 'osystems', 'program_languages', 'testing_types', 'browsers', 'description']

    def save(self, *args, **kwargs):
        """Обновление тестера с учетом смены пароля"""
        assert(self.is_valid())
        # Вызов оригинального save
        data = self.cleaned_data
        tester = super(TesterDetailForm, self).save(*args, **kwargs)
        # Проверка на смену пароля
        if data['password']:
            # Пароль изменился
            user = tester.user
            user.set_password(data['password'])
            user.save()
        
        return tester

    def clean(self):
        # Вызов оригинального clean()
        data = super(TesterDetailForm, self).clean()
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return data


# XXX:
# Предпросмотр форм
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect

class StupidFormPreview(FormPreview):
    def done(self, request, cleaned_data):
        return HttpResponseRedirect('/')

