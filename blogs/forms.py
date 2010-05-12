# File encoding: utf-8
from django import forms

# все ниже хрень

from django.contrib.auth.models import User
from markdown import markdown

from blogs.models import Blog, BlogMsg


from lib.fields import UrtestTextAreaField


class BlogEntryForm(forms.ModelForm):
    """
    Форма добавления сообщения
    """
    name = forms.CharField(label='Название', max_length=50)
    size = forms.IntegerField(label='Размер в SLOC')

    program_languages = forms.ModelMultipleChoiceField(
        label="ЯП",
        queryset=ProgramLanguage.objects.all(),
        widget=CheckboxSelectMultiple)
    
    doc_languages = forms.ModelMultipleChoiceField(
        label="Язык документации",
        queryset=Language.objects.all(),
        widget=CheckboxSelectMultiple)
    
    description = UrtestTextAreaField(
        label='Описание проекта',
        required=False)

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
    
    def save(self, customer, *args, **kwargs):
        # Проверки типов
        assert isinstance(customer, Customer)
        
        # Установка поля заказчика и сохранение
        project = super(ProjectForm, self).save(commit=False,*args, **kwargs)
        project.customer = customer
        project.save()
        # В форме есть поля много-много, требуется вызывать после сохранения
        self.save_m2m()
        return project


