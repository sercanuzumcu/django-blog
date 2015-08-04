from django.db import models
from django import forms
from django.db.models import ImageField
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s' % self.title


class Comment(models.Model):
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    cevap = models.ManyToManyField("self", null=True, blank=True)
    like = models.IntegerField()

    def __unicode__(self):
        return '%s' % self.body


class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    category = models.ManyToManyField(Category)
    comment = models.ManyToManyField(Comment)
    image = models.ImageField(upload_to='photos', blank=True)

    def __unicode__(self):
        return '%s' % self.title


class Userprofile(models.Model):
    resim = models.ImageField(upload_to='photos', blank=True)
    user = models.ForeignKey(User)

class Friend(models.Model):
    arkadas = models.ForeignKey(User)
    eklenen_arkadas = models.ForeignKey(User, related_name="eklenen_arkadas"  )
    
    def __unicode__(self):
        return '%s' % self.eklenen_arkadas.username
