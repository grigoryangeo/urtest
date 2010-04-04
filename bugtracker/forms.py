# File encoding: utf-8
from django import forms

from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple

from bugtracker.models import Bug, Project
from accounts.models import Tester, Customer
from enumerations.models import ProgramLanguage, Language


class ProjectForm(forms.ModelForm):
    """
    Форма добавления проекта
    """
    name = forms.CharField(label='Название', max_length=50)
    size = forms.IntegerField(label='Размер в SLOC')

    program_languages = forms.ModelMultipleChoiceField(
        label="ЯП",
        queryset=ProgramLanguage.objects.all(),
        widget=FilteredSelectMultiple(u'ЯП', False))
    
    doc_languages = forms.ModelMultipleChoiceField(
        label="Язык документации",
        queryset=Language.objects.all(),
        widget=FilteredSelectMultiple(u'Языки', False))
    
    description = forms.CharField(label='Описание проекта',
                                  widget=forms.Textarea,
                                  required=False,
                                  max_length=300)

    def clean_name(self):
        name = self.cleaned_data.get('name')

        try:
            Project.objects.get(name=name)
        except Project.DoesNotExist:
            return name
        raise forms.ValidationError('Проект с таким названием уже существует')

    class Meta:
        model = Project
        fields = ['name', 'size', 'program_languages', 'doc_languages', 'description']
    
    def save(self, customer=None, *args, **kwargs):
        # Проверки типов
        assert customer is Customer
        
        # Установка поля заказчика и сохранение
        project = super(ProjectForm, self).save(*args, **kwargs)
        project.customer = customer
        project.save()
        # В форме есть поля много-много, требуется вызывать после сохранения
        self.save_m2m()


class BugForm(forms.ModelForm):
    """
    Форма добавления бага
    """
    short_description = forms.CharField(label="Краткое описание",
                                        max_length=100)
    severity = forms.CharField(label="Критичность",
                               widget=forms.RadioSelect(choices=Bug.SEVERITY_CHOICES))
    finding_description = forms.CharField(label="Как был получен",
                                        widget=forms.Textarea,
                                        max_length=600)
    full_description = forms.CharField(label="Описание",
                                     widget=forms.Textarea,
                                     max_length=600)

    class Meta:
        model = Bug
        exclude = ['tester', 'status', 'status_comment', 'project']
    
    def save(self, project=None, tester=None, *args, **kwargs):
        # Проверки типов
        assert tester is Tester
        assert project is Project
        
        # Вызов родительского метода save
        bug = super(BugForm, self).save(*args, commit=False, **kwargs)

        # Установка отсутствующих в форме полей автора и проекта и сохранение
        # Они хранятся в request, к которому из формы доступа нет,
        # Поэтому передаем их как параметры save
        bug.tester = tester
        bug.project = project
        bug.save()


class BugDetail(forms.ModelForm):
    """
    Форма редактирования статуса бага
    """
    status = forms.CharField(label="Статус",
                             widget=forms.RadioSelect(choices=Bug.STATUS_CHOICES))
    status_comment = forms.CharField(label="Примечание",
                                     widget=forms.Textarea,
                                     required=False,
                                     max_length=100)
    
    class Meta:
        model = Bug
        fields = ['status', 'status_comment']
