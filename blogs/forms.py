# File encoding: utf-8
from django import forms

from markdown import markdown
from lib.fields import UrtestTextAreaField

from blogs.models import BlogEntry

from lib.fields import UrtestTextAreaField


class BlogEntryForm(forms.ModelForm):
    """
    Форма добавления сообщения
    """
    title = forms.CharField(label='Заголовок', max_length=50, required=False)
    entry = UrtestTextAreaField(label='сообщение', required=True)

    class Meta:
        model = BlogEntry
        fields = ['title', 'entry']
    
    def save(self, blog, *args, **kwargs):
        assert(self.is_valid())
        Entry = super(BlogEntryForm, self).save(commit=False,*args, **kwargs)
        Entry.entry_html = markdown(Entry.entry)
        if Entry.title == '':
            Entry.title = "Сообщение в блог"
        Entry.blog = blog
        Entry.save()
        return Entry


