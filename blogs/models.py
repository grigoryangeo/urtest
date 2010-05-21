# File encoding: utf-8
from django.db import models

class Blog(models.Model):
    """Модель блога"""
    title = models.CharField("название", max_length=80)

    class Meta:
        verbose_name = u"блог"
        verbose_name_plural = u"блоги"

    @models.permalink
    def get_absolute_url(self):
        return ('blogs.views.blog_show', (), {'blog_id': self.pk, 'entry_number': 0})

    def get_owner(self):
        try :
            return self.customer
        except models.ObjectDoesNotExist:
            pass
        try:
            return self.tester
        except models.ObjectDoesNotExist:
            pass
        try:
            return self.project
        except models.ObjectDoesNotExist:
            pass

    @property
    def owner(self):
        return self.get_owner()

    def __unicode__(self):
        return self.title


class BlogEntry(models.Model):
    """Модель сообщения блога"""
    blog = models.ForeignKey(Blog, related_name='entries',
                             verbose_name="блог")
    submit_date = models.DateField("дата", auto_now_add=True)
    title = models.CharField("заголовок", max_length=80)
    # в markdown
    entry = models.TextField("сообщение")
    # в html
    entry_html = models.TextField("сообщение", editable=False)


    class Meta:
        verbose_name = u"сообщение"
        verbose_name_plural = u"сообщения"
        ordering = ['-submit_date']

    def __unicode__(self):
        return self.title
