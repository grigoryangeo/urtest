# File encoding: utf-8
from django.db import models
from markdown import markdown
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Blog(models.Model):
    """Модель блога"""
    title = models.CharField("название", max_length=80)

    # Поля для связи Блог-Проект/Юзер через GenericForeignKey
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = u"блог"
        verbose_name_plural = u"блоги"

    def __unicode__(self):
        return self.title


class BlogEntry(models.Model):
    """Модель сообщения блога"""
    blog = models.ForeignKey(Blog, related_name='entries',
                             verbose_name="блог")
    submit_date = models.DateField("дата", auto_now_add=True)
    title = models.CharField("заголовок", max_length=80)
    # в markdown
    entry = models.TextField("сообщение", blank=True)
    # в html
    entry_html = models.TextField("сообщение", blank=True, editable=False)


    
    class Meta:
        verbose_name = u"сообщение"
        verbose_name_plural = u"сообщения"
        ordering = ['-submit_date']

    def save(self, force_insert=False, force_update=False):
        self.entry_html = markdown(self.entry)
        # Само сохранение
        super(BlogEntry, self).save(force_insert, force_update)


    def __unicode__(self):
        return self.title
