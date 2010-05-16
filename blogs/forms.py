# File encoding: utf-8
from django import forms

# все ниже хрень

from django.contrib.auth.models import User
from markdown import markdown

from blogs.models import Blog, BlogEntry


from lib.fields import UrtestTextAreaField


class BlogEntryForm(forms.ModelForm):
    """
    Форма добавления сообщения
    """
    title = forms.CharField(label='Заголовок', max_length=50)
    entry = UrtestTextAreaField(
        label='сообщение',
        required=False)

    class Meta:
        model = BlogEntry
        fields = ['title', 'entry']
    
    def save(self, blog, *args, **kwargs):
        Entry = super(BlogEntryForm, self).save(commit=False,*args, **kwargs)
        Entry.entry_html = markdown(Entry.entry)
        if Entry.title == '':
            Entry.title = "Сообщение в блог"
        Entry.blog = blog
        Entry.save()
        return Entry


