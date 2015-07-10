from django.db import models
from django import forms


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s' % self.title


class Comment(models.Model):
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    cevap = models.ManyToManyField("self", null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.body


class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    category = models.ManyToManyField(Category)
    comment = models.ManyToManyField(Comment)

    def __unicode__(self):
        return '%s' % self.title
